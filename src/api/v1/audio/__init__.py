from flask import Blueprint
audio_bp = Blueprint('audio', __name__)
from . import dfpwm, pcm
