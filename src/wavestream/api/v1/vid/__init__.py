from flask import Blueprint
vid_bp = Blueprint('vid', __name__)
from . import qtccv, sanjuuni_raw, vid32
