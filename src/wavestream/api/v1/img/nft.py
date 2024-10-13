from . import img_bp
import requests
import numpy as np
from flask import Response, request
from PIL import Image
from wavestream.utils import decode_urlsafe_base64

CC_COLORS = [
    (240, 240, 240), (242, 178, 51), (229, 127, 216), (153, 178, 242),
    (222, 222, 108), (127, 204, 25), (242, 178, 204), (76, 76, 76),
    (153, 153, 153), (76, 153, 178), (178, 102, 229), (51, 102, 204),
    (127, 102, 76), (87, 166, 78), (204, 76, 76), (25, 25, 25)
]

palette = Image.new("P", (1, 1))
palette.putpalette(
    [value for color in CC_COLORS for value in color] +
    list(CC_COLORS[-1]) * (256 - len(CC_COLORS))
)

@img_bp.route('/nft')
def get_data():
    # TODO: add more dither methods
    # TODO: Set max width, height
    width = int(request.args.get("width", 51))
    height = int(request.args.get("height", 19))
    dither = request.args.get("dither", "false").lower() == "true"
    url = request.args.get("url")
    url_is_base64 = request.args.get("urlIsBase64", "false").lower() == "true"
    if url_is_base64:
        url = decode_urlsafe_base64(url)

    img = Image.open(requests.get(url, stream=True).raw)
    quantized_image = img.resize((width, height)).convert("RGB").quantize(palette=palette, dither=dither)
    image_data = np.array(quantized_image.getdata()).reshape(height, width)
    response_data = "\n".join("".join(format(pixel, "x") for pixel in row) for row in image_data)

    return Response(response_data, mimetype="text/plain")
