# conftest.py
#
# This file is used to setup test fixtures
# for the 'pytest' unit testing framework.

import os
import sys
sys.path.insert(0, os.getcwd())

import pytest
from api import create_app


@pytest.fixture
def app():
    # if not os.path.exists("db/test.db"):
    #     raise Exception("no testing database")
    # dbtype = os.getenv('DATABASE_TYPE', 'sqlite').lower()
    # if dbtype == 'sqlite' or dbtype == 'sqlite3':
    #     uri = f'sqlite:///db/test.db'
    # else:
    u = os.getenv("POSTGRES_USER")
    pw = os.getenv('POSTGRES_PASSWORD')
    h = os.getenv('POSTGRES_HOST', 'localhost')
    p = os.getenv('POSTGRES_PORT', 5432)
    db = os.getenv('POSTGRES_DB')
    uri = f'postgresql://{u}:{pw}@{h}:{p}/{db}'
    app = create_app({
        'ENV': 'development',
        'DEBUG': False,
        'TESTING': True,
        # 'SQLALCHEMY_DATABASE_URI': f'sqlite:///db/test.db',
        'SQLALCHEMY_DATABASE_URI': uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': True, # database logging
    })

    yield app
    # Cleanup code here...
    # Close the database connection
    return


@pytest.fixture
def client(app):
    return app.test_client()
