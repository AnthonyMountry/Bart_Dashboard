import os
import os.path
import subprocess
import click

from flask.cli import with_appcontext
from flask import current_app
from db.clean import clean
from pprint import pprint
from api.user import create_user


@click.command('config', short_help='get config info')
@click.argument('args', nargs=-1)
@with_appcontext
def config(args):
    if args:
        for a in args:
            print(current_app.config[a])
    else:
        pprint(current_app.config)


@click.command('clean-data')
@click.option('--clean-meters', is_flag=True, default=False, help='generate meter data (takes a long time)')
def clean_data(clean_meters):
    click.echo('cleaning data...')
    clean('db/UC Merced 2020 SE Project', 'db/cleaned', clean_meters)
    click.echo('done.')


@click.command('load-db', short_help='Clean the data and load it into the database')
@with_appcontext
def load_db():
    type = current_app.config['DATABASE_TYPE']
    if type == 'postgres' or type == 'postgresql':
        args = ['psql', current_app.config['SQLALCHEMY_DATABASE_URI'], '-c', '\i db/pg_load.sql']
    elif  type == 'sqlite' or type == 'sqlite3':
        args = ["sqlite3", current_app.config['SQLITE_FILE'], ".read db/load.sql"]
    else:
        args = []
    subprocess.run(args)


@click.command('add-user', short_help='Add a user')
@click.option('-n', '--name', required=True, prompt=True)
@click.option('-p', '--password',
              required=True,
              prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('-e', '--email', required=False)
@click.option('--is-admin', is_flag=True, default=False, help='create a user with admin privileges')
@with_appcontext
def add_user(name, password, email, is_admin):
    if len(password) < 8:
        click.echo('password must be 8 characters or more')
        return 1
    u = create_user(name, email, password, is_admin)
    click.echo(u)

