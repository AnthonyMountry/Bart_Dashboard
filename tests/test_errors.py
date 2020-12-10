import pytest

from flask import Flask
from werkzeug.exceptions import NotFound
from api.errors import handle_notfound, handle_not_impl, handle_all

def test_error_handlers(app: Flask):
    with app.app_context():
        handle_notfound(NotFound("hello"))
        handle_all(Exception("testing"))
