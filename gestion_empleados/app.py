import os
from flask import Flask


def create_app():

    app = Flask(__name__)

    app.secret_key = "misiontic2022"  # os.urandom( 24 )
    from views import main
    from api import api

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/miApi")

    return app
