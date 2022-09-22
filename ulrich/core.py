import yaml

from flask import Flask

from . import database


def create_app(conf_file_path):

    app = Flask(__name__)

    app.config.from_file(conf_file_path, load=yaml.safe_load)

    app.db = database.Database(app.config["SQLALCHEMY_DATABASE_URI"])
    app.db.create_database()
    app.db.create_tables()

    return app
