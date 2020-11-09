import click
from flask import Flask

from api import asset
from api.config import Config
from api.util import ModelEncoder
from api.app import blueprint, db, migrate


def create_app(conf=None):
    app = Flask(__name__, static_url_path='/public')
    if conf is None:
        app.config.from_object(Config())
    else:
        app.config.from_mapping(conf)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    app.register_blueprint(asset.blueprint)
    app.register_blueprint(blueprint)
    app.json_encoder = ModelEncoder
    app.cli.add_command(init_cmd)
    return app


@click.command('init', short_help='Run all the api setup in one command')
def init_cmd():
    print('initializing app...')
    # TODO figure out how to run the database
    # migration commands here
    print('done')
