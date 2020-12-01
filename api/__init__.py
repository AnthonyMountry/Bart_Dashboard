from flask import Flask
from werkzeug.exceptions import NotFound

import os.path

from api import commands, asset, wo, errors, ui
from api.config import read_config
from api.util import ModelEncoder, ModelResponse
from api.app import blueprint

app_context = None


def create_app(conf=None):
    app = Flask(
        __name__,
        static_url_path='/public',
        static_folder='public',
    )

    if isinstance(conf, str):
        conf = read_config(conf)
    elif conf is None:
        conf = read_config('api.ini')

    app.root_path = os.getcwd()
    # app.root_path = os.path.dirname(app.root_path)
    # app.config['STATIC_DIR'] = 'public'

    from api.database import db, migrate
    with app.app_context():
        app.config.from_mapping(conf)
        db.init_app(app)
        migrate.init_app(app, db)

    app.json_encoder = ModelEncoder
    # app.response_class =  ModelResponse
    app_context = app.app_context

    app.register_blueprint(asset.blueprint)
    app.register_blueprint(wo.blueprint)
    app.register_blueprint(ui.blueprint)
    app.register_blueprint(blueprint)

    app.register_error_handler(Exception, errors.handle_all)
    app.register_error_handler(NotFound, errors.handle_notfound)
    app.register_error_handler(NotImplementedError, errors.handle_not_impl)

    app.cli.add_command(commands.init_cmd)
    app.cli.add_command(commands.load_db_cmd)
    app.cli.add_command(commands.test_cmd)
    return app


def _read_only_db(*args, **kwargs):
    # https://writeonly.wordpress.com/2009/07/16/simple-read-only-sqlalchemy-sessions/
    # for testing, maybe
    return # do nothing
