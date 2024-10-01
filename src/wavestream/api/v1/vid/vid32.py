from flask import Response
from . import vid_bp

@vid_bp.route('/32vid')
def stream_32vid():
    return Response("WIP")
