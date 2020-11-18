import pytest
from flask.wrappers import Response

def test_pages(client):
    for endpoint in ['/', '/reports', '/analytics']:
        resp: Response = client.get(endpoint)
        assert resp.status_code == 200

def test_static(client):
    resp: Response = client.get('/js/upload.js')
    assert resp.status_code == 200
    resp: Response = client.get('/img/favicon.ico')
    assert resp.status_code == 200
    resp: Response = client.get('/css/styles.css')
    assert resp.status_code == 200
