import pytest
from flask.wrappers import Response

def test_pages(client):
    # just need to make sure these exist
    for endpoint in ['/', '/dashboard', '/login', '/analytics']:
        resp: Response = client.get(endpoint)
        assert resp.status_code == 200

def test_static(client):
    resp: Response = client.get('/public/js/upload.js')
    assert resp.status_code == 200
    resp: Response = client.get('/public/img/favicon.ico')
    assert resp.status_code == 200
    resp: Response = client.get('/public/css/styles.css')
    assert resp.status_code == 200
