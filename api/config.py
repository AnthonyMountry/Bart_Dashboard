import os
from os.path import join as path_join
from iniconfig import IniConfig

from dotenv import load_dotenv
load_dotenv()


def read_config(filename):
    config = {
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'DEBUG': False,
        'TESTING': False,
        'STATIC_DIR':  '../public',
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': False,
        'COMPRESS_REGISTER': True,
    }
    if not os.path.exists(filename):
        return config

    ini = IniConfig(filename)

    tmpl_reload = ini.get("server", 'template_reload')
    if tmpl_reload:
        tmpl_reload = tmpl_reload.lower()
        config["TEMPLATES_AUTO_RELOAD"] = tmpl_reload == 'true' or tmpl_reload == 'yes'

    debug = ini.get('server', 'debug')
    if debug is not None:
        config['DEBUG'] = debug.lower() == 'true' or debug.lower() == 'yes'
    dbtype = ini.get('database', 'type', os.getenv("DATABASE_TYPE"))
    dbfile = ini.get('database', 'file')
    config['DATABASE_TYPE'] = dbtype
    if dbtype is None or dbtype == 'sqlite':
        if dbfile is None:
            config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        else:
            config['SQLALCHEMY_DATABASE_URI'] = path_join('sqlite:///', dbfile)
            config['SQLITE_FILE'] = dbfile
    elif dbtype.lower() == 'postgres' or dbtype in {'postgres', 'postgresql'}:
        u = ini.get('database', 'username', os.getenv("POSTGRES_USER"))
        p = ini.get('database', 'password', os.getenv('POSTGRES_PASSWORD'))
        h = ini.get('database', 'host', 'localhost')
        port = ini.get('database', 'port', os.getenv('POSTGRES_PORT')) or 5432
        name = ini.get('database', 'name', os.getenv('POSTGRES_DB'))
        url = path_join(f'{h}:{port}', name)
        config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{u}:{p}@{url}'
        config['POSTGRES_USER'] = u
        config['POSTGRES_PASSWORD'] = p
        config['POSTGRES_HOST'] = h
        config['POSTGRES_PORT'] = port
        config['POSTGRES_DB'] = name

    return config
