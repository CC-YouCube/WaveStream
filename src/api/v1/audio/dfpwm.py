from flask import Response, request, stream_with_context
from subprocess import Popen, PIPE, DEVNULL
from yt_dlp import YoutubeDL
from . import audio_bp

ydl_opts = {
    "format": "worstaudio*",
    "quiet": True,
    "default_search": "auto",
    "extract_flat": "in_playlist"
}

# TODO; auth, spotify, stremlink
def get_stream(url: str) -> str:
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
        # TODO: very good code ;)
        if data.get("_type") == "playlist":
            return ydl.extract_info(data.get("entries")[0].get("url"), download=False).get("url")
        return data.get("url")

# TODO: support stereo and 5.1 (if possible)
# TODO: Allow real seeking (if possible)

@audio_bp.route('/dfpwm')
def stream_dfpwm():
    # TODO: add option to seek before
    url = request.args.get("url")
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
        stderr=DEVNULL,
        bufsize=8*16 # TODO: Find optimal buffer size
    )

    @stream_with_context
    def generate():
        while True:
            data = process.stdout.read(8*16)
            # TODO: Fix Noise at EOF
            if not data:
                break
            yield data

    return Response(
        generate(),
        mimetype="audio/dfpwm;rate=48000;channels=1",
        headers={"Content-Disposition": 'attachment;filename="audio.dfpwm"'}
    )
