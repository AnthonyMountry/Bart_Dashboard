from flask import (
    Blueprint,
    jsonify,
    request as req,
)

from ..extensions import bcrypt, db
from .models import User

blueprint = Blueprint('user', __name__)

def get_user(username=None, email=None):
    if not username and not email:
        return None
    res = User.query
    if username:
        res = res.filter(User.username == username)
    if email:
        res = res.filter(User.email == email)
    user = res.first()
    if not user:
        return None
    return user

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

    u = get_user(username, email)
    if not u:
        return {'error': 'could not find user'}, 404

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
        db.session.delete(u)
        db.session.commit()
        return {"status": 200, 'msg': "user delete"}, 200


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

    u = get_user(username, req.json.get('email', None))
    if u is not None:
        return {'error': 'user already exists'}, 400
    u = create_user(username, req.json.get('email'), pw, False)
    return jsonify(u), 201
