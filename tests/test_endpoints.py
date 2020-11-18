import pytest

from flask import Flask
from flask.wrappers import Response


def test_app(app: Flask):
    pass

def test_assets(client):
    resp: Response = client.get('/api/assets?limit=12')
    assert len(resp.json) == 1
    assert len(resp.json['assets']) == 12
    prev = resp

    resp = client.get('/api/assets?limit=5&offset=4')
    assert len(resp.json) == 1
    assert len(resp.json['assets']) == 5

    for key in ['num', 'status', 'description', 'bartdept']:
        assert resp.json['assets'][0][key] == prev.json['assets'][4][key]


def test_asset(client):
    resp: Response = client.get('/api/asset/15384437')
    assert resp.status_code == 200
    assert resp.json['num'] == 15384437

def test_bad_asset(client):
    resp = client.get('/api/asset/0')
    assert resp.status_code == 404

def test_asset_readings(client):
    resp: Response = client.get('/api/asset/15384437/readings')
    assert resp.status_code == 200
    assert resp.json['num'] == 15384437

def test_workorders(client):
    resp: Response = client.get('/api/workorders?limit=10')
    assert resp.status_code == 200
    assert len(resp.json['workorders']) == 10

    num = resp.json['workorders'][0]['num']
    resp: Response = client.get(f'/api/workorder/{num}')
    assert resp.json
    assert resp.json['num'] == num

def test_bad_workorder(client):
    resp = client.get('/api/workorder/0')
    assert resp.status_code == 404