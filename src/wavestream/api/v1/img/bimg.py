from flask import Response
from . import img_bp

@img_bp.route('/bimg')
def stream_bimg():
    # see https://github.com/MCJack123/sanjuuni/pull/28
    return Response("WIP")
