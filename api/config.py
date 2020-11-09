import os
from os.path import join as path_join
from iniconfig import IniConfig


class Config:
    """
    Setup API configuration.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/dashboard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = False

    def __init__(self, config_file='api.ini'):
        self.ini = IniConfig(config_file)
        debug = self.ini.get('server', 'debug')
        if debug is not None:
            self.DEBUG = debug.lower() == 'true' or debug.lower() == 'yes'
        dbtype = self.ini.get('database', 'type')
        dbfile = self.ini.get('database', 'file')
        if dbtype is None or dbtype == 'sqlite':
            if dbfile is None:
                Config.SQLALCHEMY_DATABASE_URI = 'sqlite://' # in-memory sqlite
            else:
                Config.SQLALCHEMY_DATABASE_URI = path_join('sqlite:///', dbfile)
        elif dbtype in {'postgres', 'postgresql'}:
            u = self.ini.get('database', 'username')
            p = self.ini.get('database', 'password')
            h = self.ini.get('database', 'host')
            port = self.ini.get('database', 'port', 5432)
            name = self.ini.get('database', 'name', '')
            url = path_join(f'{h}:{port}', name)
            Config.SQLALCHEMY_DATABASE_URI = f'postgresql://{u}:{p}@{url}'
            Config.DB_TYPE = 'postgresql'
