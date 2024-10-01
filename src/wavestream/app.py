from os import getenv

from flask import Flask, Response
from .api.v1 import v1

app = Flask(__name__, static_url_path='')

app.register_blueprint(v1, url_prefix="/api/v1")

# TODO: only with auth and prio "account"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('404.html'), 404

def main():
    app.run(
        host=getenv("HOST"),
        port=getenv("PORT"),
        debug=getenv("DEBUG")
    ) # TODO: run threaded and use real wsgi server

if __name__ == '__main__':
    main()
