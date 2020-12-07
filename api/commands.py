import os
import os.path
import subprocess
import click

from flask.cli import with_appcontext
from flask import current_app
from db.clean import clean
import json
from pprint import pprint

@click.command("test", short_help='test', hidden=True)
def test_cmd():
    ...

@click.command('config', short_help='get config info')
@click.argument('args', nargs=-1)
@with_appcontext
def config(args):
    if args:
        for a in args:
            print(current_app.config[a])
    else:
        pprint(current_app.config)


@click.command('load-db', short_help='Clean the data and load it into the database')
@click.option("--db", default='db/dashboard.db', help='output database file', show_default=True)
@click.option('--clean-meters', is_flag=True, default=False, help='generate meter data (takes a long time)')
@click.option('--skip-insert', default=False, is_flag=True, help='skip inserts')
@with_appcontext
def load_db_cmd(db, clean_meters, skip_insert):
    click.echo('cleaning data...')
    clean('db/UC Merced 2020 SE Project', 'db/cleaned', clean_meters)

    click.echo("loading data...")
    if not skip_insert:
        type = current_app.config['DATABASE_TYPE']
        if type == 'postgres' or type == 'postgresql':
            args = [
                'psql',
                current_app.config['SQLALCHEMY_DATABASE_URI'],
                '-c', '\i db/postgres/02-load.sql',
            ]
        elif  type == 'sqlite' or type == 'sqlite3':
            args = ["sqlite3", db, ".read db/load.sql"]
        else:
            args = []
        subprocess.run(args)
    click.echo('done.')


@click.command('init', short_help='Run all the api setup in one command')
def init_cmd():
    print('initializing app...')
    # TODO figure out how to run the database
    # migration commands here

    print('done')
