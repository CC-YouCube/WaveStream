from flask import Response
from . import vid_bp

@vid_bp.route('/sanjuuni.raw')
def stream_sanjuuni_raw():
    return Response("WIP")
