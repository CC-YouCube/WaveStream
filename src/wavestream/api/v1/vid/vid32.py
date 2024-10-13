from flask import Response
from . import vid_bp

@vid_bp.route('/32vid')
def stream_32vid():
    # see https://github.com/MCJack123/sanjuuni/issues/29
    return Response("WIP")
