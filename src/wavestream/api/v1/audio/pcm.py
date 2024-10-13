from flask import Response, request, stream_with_context, current_app
from subprocess import Popen, PIPE, DEVNULL
from . import audio_bp
from wavestream.utils import get_stream, decode_urlsafe_base64

# TODO: support stereo and 5.1 (if possible)
# TODO: Allow real seeking (if possible)

""" PCM formats
 DE  alaw            PCM A-law
 DE  f32be           PCM 32-bit floating-point big-endian
 DE  f32le           PCM 32-bit floating-point little-endian
 DE  f64be           PCM 64-bit floating-point big-endian
 DE  f64le           PCM 64-bit floating-point little-endian
 DE  mulaw           PCM mu-law
 DE  s16be           PCM signed 16-bit big-endian
 DE  s16le           PCM signed 16-bit little-endian
 DE  s24be           PCM signed 24-bit big-endian
 DE  s24le           PCM signed 24-bit little-endian
 DE  s32be           PCM signed 32-bit big-endian
 DE  s32le           PCM signed 32-bit little-endian
 DE  s8              PCM signed 8-bit
 DE  u16be           PCM unsigned 16-bit big-endian
 DE  u16le           PCM unsigned 16-bit little-endian
 DE  u24be           PCM unsigned 24-bit big-endian
 DE  u24le           PCM unsigned 24-bit little-endian
 DE  u32be           PCM unsigned 32-bit big-endian
 DE  u32le           PCM unsigned 32-bit little-endian
 DE  u8              PCM unsigned 8-bit
 DE  vidc            PCM Archimedes VIDC
"""

""" codecs
 D.AIL. adpcm_4xm            ADPCM 4X Movie
 DEAIL. adpcm_adx            SEGA CRI ADX ADPCM
 D.AIL. adpcm_afc            ADPCM Nintendo Gamecube AFC
 D.AIL. adpcm_agm            ADPCM AmuseGraphics Movie AGM
 D.AIL. adpcm_aica           ADPCM Yamaha AICA
 DEAIL. adpcm_argo           ADPCM Argonaut Games
 D.AIL. adpcm_ct             ADPCM Creative Technology
 D.AIL. adpcm_dtk            ADPCM Nintendo Gamecube DTK
 D.AIL. adpcm_ea             ADPCM Electronic Arts
 D.AIL. adpcm_ea_maxis_xa    ADPCM Electronic Arts Maxis CDROM XA
 D.AIL. adpcm_ea_r1          ADPCM Electronic Arts R1
 D.AIL. adpcm_ea_r2          ADPCM Electronic Arts R2
 D.AIL. adpcm_ea_r3          ADPCM Electronic Arts R3
 D.AIL. adpcm_ea_xas         ADPCM Electronic Arts XAS
 DEAIL. adpcm_g722           G.722 ADPCM (decoders: g722) (encoders: g722)
 DEAIL. adpcm_g726           G.726 ADPCM (decoders: g726) (encoders: g726)
 DEAIL. adpcm_g726le         G.726 ADPCM little-endian (decoders: g726le) (encoders: g726le)
 D.AIL. adpcm_ima_acorn      ADPCM IMA Acorn Replay
 DEAIL. adpcm_ima_alp        ADPCM IMA High Voltage Software ALP
 DEAIL. adpcm_ima_amv        ADPCM IMA AMV
 D.AIL. adpcm_ima_apc        ADPCM IMA CRYO APC
 DEAIL. adpcm_ima_apm        ADPCM IMA Ubisoft APM
 D.AIL. adpcm_ima_cunning    ADPCM IMA Cunning Developments
 D.AIL. adpcm_ima_dat4       ADPCM IMA Eurocom DAT4
 D.AIL. adpcm_ima_dk3        ADPCM IMA Duck DK3
 D.AIL. adpcm_ima_dk4        ADPCM IMA Duck DK4
 D.AIL. adpcm_ima_ea_eacs    ADPCM IMA Electronic Arts EACS
 D.AIL. adpcm_ima_ea_sead    ADPCM IMA Electronic Arts SEAD
 D.AIL. adpcm_ima_iss        ADPCM IMA Funcom ISS
 D.AIL. adpcm_ima_moflex     ADPCM IMA MobiClip MOFLEX
 D.AIL. adpcm_ima_mtf        ADPCM IMA Capcom's MT Framework
 D.AIL. adpcm_ima_oki        ADPCM IMA Dialogic OKI
 DEAIL. adpcm_ima_qt         ADPCM IMA QuickTime
 D.AIL. adpcm_ima_rad        ADPCM IMA Radical
 D.AIL. adpcm_ima_smjpeg     ADPCM IMA Loki SDL MJPEG
 DEAIL. adpcm_ima_ssi        ADPCM IMA Simon & Schuster Interactive
 DEAIL. adpcm_ima_wav        ADPCM IMA WAV
 DEAIL. adpcm_ima_ws         ADPCM IMA Westwood
 DEAIL. adpcm_ms             ADPCM Microsoft
 D.AIL. adpcm_mtaf           ADPCM MTAF
 D.AIL. adpcm_psx            ADPCM Playstation
 D.AIL. adpcm_sbpro_2        ADPCM Sound Blaster Pro 2-bit
 D.AIL. adpcm_sbpro_3        ADPCM Sound Blaster Pro 2.6-bit
 D.AIL. adpcm_sbpro_4        ADPCM Sound Blaster Pro 4-bit
 DEAIL. adpcm_swf            ADPCM Shockwave Flash
 D.AIL. adpcm_thp            ADPCM Nintendo THP
 D.AIL. adpcm_thp_le         ADPCM Nintendo THP (Little-Endian)
 D.AIL. adpcm_xa             ADPCM CDROM XA
 D.AIL. adpcm_xmd            ADPCM Konami XMD
 DEAIL. adpcm_yamaha         ADPCM Yamaha
 D.AIL. adpcm_zork           ADPCM Zork
 D.AIL. cbd2_dpcm            DPCM Cuberoot-Delta-Exact
 D.AIL. derf_dpcm            DPCM Xilam DERF
 D.AIL. gremlin_dpcm         DPCM Gremlin
 D.AIL. interplay_dpcm       DPCM Interplay
 DEAIL. pcm_alaw             PCM A-law / G.711 A-law
 DEAI.S pcm_bluray           PCM signed 16|20|24-bit big-endian for Blu-ray media
 DEAI.S pcm_dvd              PCM signed 20|24-bit big-endian
 D.AI.S pcm_f16le            PCM 16.8 floating point little-endian
 D.AI.S pcm_f24le            PCM 24.0 floating point little-endian
 DEAI.S pcm_f32be            PCM 32-bit floating point big-endian
 DEAI.S pcm_f32le            PCM 32-bit floating point little-endian
 DEAI.S pcm_f64be            PCM 64-bit floating point big-endian
 DEAI.S pcm_f64le            PCM 64-bit floating point little-endian

 DEAI.S pcm_s16be            PCM signed 16-bit big-endian
 DEAI.S pcm_s16be_planar     PCM signed 16-bit big-endian planar
 DEAI.S pcm_s16le            PCM signed 16-bit little-endian
 DEAI.S pcm_s16le_planar     PCM signed 16-bit little-endian planar
 DEAI.S pcm_s24be            PCM signed 24-bit big-endian

 DEAI.S pcm_s24le            PCM signed 24-bit little-endian
 DEAI.S pcm_s24le_planar     PCM signed 24-bit little-endian planar
 DEAI.S pcm_s32be            PCM signed 32-bit big-endian
 DEAI.S pcm_s32le            PCM signed 32-bit little-endian
 DEAI.S pcm_s32le_planar     PCM signed 32-bit little-endian planar
 DEAI.S pcm_s64be            PCM signed 64-bit big-endian
 DEAI.S pcm_s64le            PCM signed 64-bit little-endian
 DEAI.S pcm_s8               PCM signed 8-bit
 DEAI.S pcm_s8_planar        PCM signed 8-bit planar     ?

 DEAI.S pcm_u16be            PCM unsigned 16-bit big-endian
 DEAI.S pcm_u16le            PCM unsigned 16-bit little-endian
 DEAI.S pcm_u24be            PCM unsigned 24-bit big-endian
 DEAI.S pcm_u24le            PCM unsigned 24-bit little-endian
 DEAI.S pcm_u32be            PCM unsigned 32-bit big-endian
 DEAI.S pcm_u32le            PCM unsigned 32-bit little-endian
 DEAI.S pcm_u8               PCM unsigned 8-bit
"""

# TODO: Find optimal buffer/chunk size
CHUNK_SIZE=8*16
bufsize = CHUNK_SIZE*2 # Hope this makes sense

@audio_bp.route('/pcm')
def stream_pcm():
    # TODO: add option to seek before
    url = request.args.get("url")
    url_is_base64 = request.args.get("urlIsBase64", "false").lower() == "true"
    if url_is_base64:
        url = decode_urlsafe_base64(url)

    process = Popen(
    [
            "ffmpeg",
            "-i",
            get_stream(url),
            "-f",
            "wav", # TODO: should be raw
            "-acodec",
            "pcm_u8", # TODO: support all
            "-ac",
            "1",
            "-ar",
            "48000",
            # TODO: https://stackoverflow.com/questions/16658873/how-to-minimize-the-delay-in-a-live-streaming-with-ffmpeg
            # TODO: https://superuser.com/questions/490683/cheat-sheets-and-preset-settings-that-actually-work-with-ffmpeg-1-0
            # TODO: https://ffmpeg-api.com/learn/ffmpeg/recipe/live-streaming
            # TODO: https://superuser.com/questions/155305/how-many-threads-does-ffmpeg-use-by-default
            #"-preset", "ultrafast",
            #"-tune", "zerolatency",
            #"-threads", "4",
            "-"
        ],
        stdout=PIPE,
        stderr=None if current_app.debug else DEVNULL,
        bufsize=bufsize
    )

    @stream_with_context
    def generate():
        while True:
            data = process.stdout.read(CHUNK_SIZE)
            # TODO: Fix Noise at EOF
            if not data:
                break
            yield data

    return Response(
        generate(),
        mimetype="audio/pcm;rate=48000;channels=1",
        headers={"Content-Disposition": 'attachment;filename="audio.pcm"'}
    )
# application/octet-stream