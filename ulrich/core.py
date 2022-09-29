import yaml

from flask import Flask

from . import database

DEFAULT_CONF = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:////",
    "FILE_STORAGE": "_ulrich_storage",
}


def create_app(conf_file_path):

    app = Flask(__name__)

    app.config.from_mapping(DEFAULT_CONF)
    app.config.from_file(conf_file_path, load=yaml.safe_load)

    app.db = database.Database(
        dburl=app.config["SQLALCHEMY_DATABASE_URI"],
        storage_path=app.config["FILE_STORAGE"],
    )
    app.db.create_database()
    app.db.create_tables()

    return app
