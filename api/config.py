import os
from os.path import join as path_join
from iniconfig import IniConfig


def read_config(filename):
    config = {
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'DEBUG': False,
        'TESTING': False,
    }
    if not os.path.exists(filename):
        return config

    ini = IniConfig(filename)
    debug = ini.get('server', 'debug')
    if debug is not None:
        config['DEBUG'] = debug.lower() == 'true' or debug.lower() == 'yes'
    dbtype = ini.get('database', 'type')
    dbfile = ini.get('database', 'file')
    if dbtype is None or dbtype == 'sqlite':
        config['BD_TYPE'] = 'sqlite'
        if dbfile is None:
            config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        else:
            config['SQLALCHEMY_DATABASE_URI'] = path_join('sqlite:///', dbfile)
    elif dbtype in {'postgres', 'postgresql'}:
        u = ini.get('database', 'username')
        p = ini.get('database', 'password')
        h = ini.get('database', 'host')
        port = ini.get('database', 'port', 5432)
        name = ini.get('database', 'name', '')
        url = path_join(f'{h}:{port}', name)
        config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{u}:{p}@{url}'
        config['DB_TYPE'] = 'postgresql'
    return config