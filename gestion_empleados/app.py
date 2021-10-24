import os
from flask import Flask, render_template


def page_not_found(e):
    return render_template("error.html"), 404


def create_app():

    app = Flask(__name__)

    app.secret_key = "misiontic2022"  # os.urandom( 24 )
    from views import main

    app.register_error_handler(404, page_not_found)
    app.register_blueprint(main)
    return app
