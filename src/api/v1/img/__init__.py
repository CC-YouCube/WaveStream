from flask import Blueprint
img_bp = Blueprint('img', __name__)
from . import nft, bimg
