import pytest

from flask.wrappers import Response
from flask.testing import FlaskClient

def test_ui_handlers(client):
    urls = [
        "/asset?assetnum=15384437",
        "/notifications",
        "/search?q=swat",
        "/login",
        "/dashboard",
        "/analytics",
        "/",
    ]
    for url in urls:
        resp: Response = client.get(url)
        assert resp.status_code == 200
        assert resp.data.decode("utf-8").startswith('<!DOCTYPE html>')

def test_static(client):
    resp: Response = client.get('/public/js/upload.js')
    assert resp.status_code == 200
    resp: Response = client.get('/public/img/favicon.ico')
    assert resp.status_code == 200
    resp: Response = client.get('/public/css/styles.css')
    assert resp.status_code == 200

def test_login(client: FlaskClient):
    resp: Response = client.post(
        '/login',
        content_type='application/x-www-form-urlencoded',
        data={'username': 'test-user', 'password': 'testing1234'}
    )
    assert resp.status_code == 302 # redirect to dashboard
    assert '/dashboard' in resp.location

    bad_data = [
        {'username': '__bad-test-user__', 'password': 'badpassword'},
        {'username': 'test-user', 'password': 'this-is-the-wrong-password'},
        {},
    ]
    for data in bad_data:
        resp = client.post(
            '/login', data=data,
            content_type='application/x-www-form-urlencoded',
        )
    assert resp.status_code == 401
