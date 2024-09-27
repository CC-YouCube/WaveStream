from flask import Flask, Response
from subprocess import Popen, PIPE, DEVNULL
from yt_dlp import YoutubeDL

ydl_opts = {
    "format": "worstaudio*",
    "quiet": True,
    "default_search": "auto",
    "extract_flat": "in_playlist"
}

def get_stream(url: str) -> str:
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
        # very good code ;)
        if data.get("_type") == "playlist":
            return ydl.extract_info(data.get("entries")[0].get("url"), download=False).get("url")
        return data.get("url")

app = Flask(__name__)

# support stereo and 5.1

@app.route('/yt/<v>')
def stream_audio(v: str):
    # allow format recognition by for example mpv
    if v.endswith('.dfpwm'):
        v = v[:-6]
    def generate():
        # TODO: dont process more than needed
        url = get_stream(v)
        with Popen(
                [
                    "ffmpeg",
                    "-i",
                    url,
                    "-f",
                    "dfpwm",
                    "-ac",
                    "1",
                    "-ar",
                    "48000",
                    "-"
                ],
                stdout=PIPE,
                stderr=DEVNULL
        ) as process:
            while True:
                # TODO: need to buffer
                data = process.stdout.read(16)
                if not data:
                    break
                yield data

    # kill proc on requst closr

    response = Response(generate(), mimetype="audio/dfpwm;rate=48000;channels=1")
    response.headers["Content-Disposition"] = f'attachment;filename="{v}.dfpwm"'
    return response

def main():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
