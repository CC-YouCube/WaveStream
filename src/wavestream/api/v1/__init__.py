from flask import Blueprint
from .img import img_bp
from .audio import audio_bp
from .vid import vid_bp

v1 = Blueprint('v1', __name__)
v1.register_blueprint(img_bp, url_prefix='/img')
v1.register_blueprint(audio_bp, url_prefix='/audio')
v1.register_blueprint(vid_bp, url_prefix='/vid')
