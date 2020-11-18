import os
import os.path
import subprocess
import click

from db.clean import clean

@click.command("test", short_help='test', hidden=True)
def test_cmd():
    ...


@click.command('load-db',
    short_help='Clean the data and load it into the database')
@click.option("--db", default='db/dashboard.db',
    help='output database file', show_default=True)
def load_db_cmd(db):
    if not os.path.exists("db/dashboard.db"):
        click.echo("No database!")
        click.echo("run 'flask db init', 'flask db migrate', and 'flask db upgrade'")
        return 1

    click.echo('cleaning data...')
    clean('db/UC Merced 2020 SE Project', 'db/cleaned')

    click.echo("loading data...")
    subprocess.run(
        ["sqlite3", db, ".read db/load.sql"],
    )
    click.echo('done.')


@click.command('init', short_help='Run all the api setup in one command')
def init_cmd():
    print('initializing app...')
    # TODO figure out how to run the database
    # migration commands here

    print('done')
