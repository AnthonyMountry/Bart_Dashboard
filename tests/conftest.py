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
    app = create_app({
        'ENV': 'development',
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///../db/dashboard.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': False, # database logging

        'READ_ONLY': True,
    })

    yield app
    # Cleanup code here...
    # Close the database connection
    return


@pytest.fixture
def client(app):
    return app.test_client()
