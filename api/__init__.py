import os.path
from flask import Flask

from api import commands, asset, wo
from api.config import read_config
from api.util import ModelEncoder
from api.app import blueprint
from api.database import db, migrate

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

    if not app.config['TESTING']:
        # app.root_path = os.path.dirname(app.root_path)
        app.root_path = os.getcwd()
        app.config['STATIC_DIR'] = 'public'

    with app.app_context():
        app.config.from_mapping(conf)
        db.init_app(app)
        migrate.init_app(app, db)

    app.register_blueprint(asset.blueprint)
    app.register_blueprint(wo.blueprint)
    app.register_blueprint(blueprint)
    app.json_encoder = ModelEncoder
    app.cli.add_command(commands.init_cmd)
    app.cli.add_command(commands.load_db_cmd)
    app.cli.add_command(commands.test_cmd)
    app_context = app.app_context
    return app


def _read_only_db(*args, **kwargs):
    # https://writeonly.wordpress.com/2009/07/16/simple-read-only-sqlalchemy-sessions/
    return # do nothing
