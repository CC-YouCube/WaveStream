from flask import Response
from . import img_bp

@img_bp.route('/bimg')
def stream_bimg():
    return Response("WIP")
