from os import getenv

from flask import Flask, Response
from api.v1 import v1 as v1_blueprint

app = Flask(__name__)

app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

# TODO: only with auth and prio "account"

@app.route("/")
def hello():
    return Response("Hello World!")

if __name__ == '__main__':
    app.run(
        host=getenv("HOST"),
        port=getenv("PORT"),
        debug=getenv("DEBUG")
    ) # TODO: run threaded and use real wsgi server
