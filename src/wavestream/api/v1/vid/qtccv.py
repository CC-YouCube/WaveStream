from flask import Response
from . import vid_bp

@vid_bp.route('/qtccv')
def stream_qtccv():
    # see https://github.com/Axisok/qtccv
    return Response("WIP")
