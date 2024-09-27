from os import getenv
import requests
import numpy as np
from flask import Flask, Response, request
from PIL import Image

app = Flask(__name__)

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

@app.route("/img.nft")
def get_data():
    width = int(request.args.get("width", 51))
    height = int(request.args.get("height", 19))
    dither = request.args.get("dither", "false").lower() == "true"
    url = request.args.get("url")

    img = Image.open(requests.get(url, stream=True).raw)
    quantized_image = img.resize((width, height)).convert("RGB").quantize(palette=palette, dither=dither)
    image_data = np.array(quantized_image.getdata()).reshape(height, width)
    response_data = "\n".join("".join(format(pixel, "x") for pixel in row) for row in image_data)

    return Response(response_data, mimetype="text/plain")

def main():
    app.run(
        host=getenv('HOST', '0.0.0.0'),
        port=int(getenv('PORT', 8000))
    )

if __name__ == "__main__":
    main()
