from os import getenv

from flask import Flask
from api.v1 import v1 as v1_blueprint

app = Flask(__name__)

app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

# TODO: only with auth and prio "account"

if __name__ == '__main__':
    app.run(
        host=getenv("HOST"),
        port=getenv("PORT"),
        debug=True # TODO: disable in prod
    ) # TODO: run threaded and use real wsgi server
