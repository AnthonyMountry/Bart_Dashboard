import pytest
import io

from flask.testing import FlaskClient
from flask.wrappers import Response

def test_upload(client: FlaskClient):
    resp: Response = client.post(
        '/api/upload',
        data={
            'file': (
                io.BytesIO(b"one,two,three\none,two,three"),
                'test.csv'
            )
        },
        follow_redirects=True,
        content_type='multipart/form-data',
    )
    assert resp.status_code == 200