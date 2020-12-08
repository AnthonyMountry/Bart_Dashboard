from flask import Flask
from werkzeug.exceptions import NotFound

from dotenv import load_dotenv
load_dotenv()

import os.path


from api import (
    commands,
    asset,
    wo,
    errors,
    ui,
    project,
    user
)
from api.config import read_config
from api.util import ModelEncoder
from api.app import blueprint, api


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
    app.json_encoder = ModelEncoder

    app.register_blueprint(project.blueprint)
    app.register_blueprint(asset.blueprint)
    app.register_blueprint(wo.blueprint)
    app.register_blueprint(ui.blueprint)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(api)
    # app.register_blueprint(blueprint)

    app.register_error_handler(Exception, errors.handle_all)
    app.register_error_handler(NotFound, errors.handle_notfound)
    app.register_error_handler(NotImplementedError, errors.handle_not_impl)

    app.cli.add_command(commands.init_cmd)
    app.cli.add_command(commands.load_db_cmd)
    app.cli.add_command(commands.test_cmd)
    app.cli.add_command(commands.config)

    from api.extensions import db, migrate, compress
    app.config.from_mapping(conf)
    db.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    return app
