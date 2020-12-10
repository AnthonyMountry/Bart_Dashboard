from flask import (
    Blueprint,
    jsonify,
    request as req,
)
from sqlalchemy import or_

from ..extensions import bcrypt, db
from .models import User

blueprint = Blueprint('user', __name__)

def create_user(name, email, pw, admin=False):
    u = User(
        username=name,
        email=email,
        is_admin=admin,
        hash=bcrypt.generate_password_hash(pw.encode("utf-8")).decode("utf-8"),
    )
    db.session.add(u)
    db.session.commit()
    return u

@blueprint.route('/api/user', methods=('GET', 'PUT', 'DELETE'))
def user():
    username = req.args.get('username') or req.args.get('user') or req.args.get('u')
    email = req.args.get('email')
    if not username and not email:
        return {'error': 'no information given'}, 400
    q = User.query
    if username:
        q = q.filter(User.username == username)
    if email:
        q = q.filter(User.email == email)

    res = q.all()
    if not res:
        return {'error': 'could not find user'}, 404
    elif len(res) > 1:
        return {'error': 'duplicate user, give more inforamtion'}, 401

    u = res[0]

    pw = req.args.get('password') or req.args.get('pw') or req.args.get('p')
    if pw is None:
        return {'error':'no password'}, 401
    if not u.password_ok(pw):
        return {'error': 'bad credentials'}, 401

    if req.method == 'GET':
        return jsonify(u), 200
    elif req.method == 'PUT':
        raise NotImplementedError
    elif req.method == 'DELETE':
        raise NotImplementedError


@blueprint.route('/api/user', methods=('POST',))
def new_user():
    if not req.json:
        return {'error': 'no user data'}, 400

    username = req.json.get('user') or req.json.get('username')
    pw = req.json.get('password') or req.json.get('pw')
    if not username:
        return {'error': 'no username'}, 400
    if not pw:
        return {'error': 'no password'}, 400

    u = create_user(username, req.json.get('email'), pw, False)
    return jsonify(u), 201

