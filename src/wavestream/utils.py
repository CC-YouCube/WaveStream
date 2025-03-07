from base64 import urlsafe_b64decode
from yt_dlp import YoutubeDL
from os import getenv

ydl_opts = {
    "format": "worstaudio*",
    "quiet": True,
    "default_search": "auto",
    "extract_flat": "in_playlist",
    "cookiefile": getenv("COOKIES")
}

# TODO: do some validation on the url
# TODO: disallow connection to localhost
# TODO: fix hls
# TODO; auth, spotify, stremlink
def get_stream(url: str) -> str:
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
        # TODO: very good code ;)
        if data.get("_type") == "playlist":
            return ydl.extract_info(data.get("entries")[0].get("url"), download=False).get("url")
        return data.get("url")

def decode_urlsafe_base64(url: str) -> str:
    """
    Decodes a URL-safe Base64 encoded string.
    Ignores padding!
    """
    return urlsafe_b64decode(url+"==").decode()
