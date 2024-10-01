from flask import Response, request, stream_with_context, current_app
from subprocess import Popen, PIPE, DEVNULL
from . import audio_bp
from wavestream.utils import get_stream, decode_urlsafe_base64

# TODO: support stereo and 5.1 (if possible)
# TODO: Allow real seeking (if possible)

# TODO: Find optimal buffer/chunk size
CHUNK_SIZE=8*16
bufsize = CHUNK_SIZE*2 # Hope this makes sense

@audio_bp.route('/dfpwm')
def stream_dfpwm():
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
            "dfpwm",
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
        mimetype="audio/dfpwm;rate=48000;channels=1",
        headers={"Content-Disposition": 'attachment;filename="audio.dfpwm"'}
    )
