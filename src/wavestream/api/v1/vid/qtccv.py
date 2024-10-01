from flask import Response
from . import vid_bp

@vid_bp.route('/qtccv')
def stream_qtccv():
    return Response("WIP")
