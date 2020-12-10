import pytest

from flask.wrappers import Response

def test_ui_handlers(client):
    urls = [
        "/asset?assetnum=15384437",
        "/notifications",
        "/search?q=swat",
        "/login",
        "/dashboard",
        "/analytics"
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