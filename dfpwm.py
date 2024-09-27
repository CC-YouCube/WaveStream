from flask import Flask, Response, request
from subprocess import Popen, PIPE, DEVNULL
from yt_dlp import YoutubeDL

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

app = Flask(__name__)

# TODO: support stereo and 5.1

@app.route('/audio.dfpwm')
def stream_audio():
    url = request.args.get("url")
    process = Popen([
        "ffmpeg",
        "-i",
        get_stream(url),
        "-f",
        "dfpwm",
        "-ac",
        "1",
        "-ar",
        "48000",
        "-"
    ], stdout=PIPE, stderr=DEVNULL)

    def generate():
        # TODO: dont process more than needed
        while True:
            # TODO: need to buffer
            data = process.stdout.read(16)
            if not data:
                break
            yield data

    # TODO: what is stream_with_context
    return Response(
        generate(),
        mimetype="audio/dfpwm;rate=48000;channels=1",
        headers={"Content-Disposition": 'attachment;filename="audio.dfpwm"'}
    )

def main():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
