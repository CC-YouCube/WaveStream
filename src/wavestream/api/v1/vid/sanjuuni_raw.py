from flask import Response
from . import vid_bp

@vid_bp.route('/sanjuuni.raw')
def stream_sanjuuni_raw():
    # see https://github.com/MCJack123/sanjuuni/issues/29
    return Response("WIP")
