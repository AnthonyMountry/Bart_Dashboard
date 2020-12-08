from flask import (
    Blueprint,
    jsonify,
    request as req,
)

from ..extensions import bcrypt, db
from .models import User

blueprint = Blueprint('user', __name__)

@blueprint.route('/api/user', methods=('GET', 'PUT', 'DELETE'))
def user():
    res = User.query.filter_by(
        username=req.args.get('user'),
        email=req.args.get('email'),
    ).all()

    if not res:
        return {'error': 'could not find user'}, 404
    u = res[0]
    if not u.password_ok(req.args.get('pw')):
        return {'error': 'bad credentials'}, 401


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
    u = User(
        username=req.args.get("user"),
        email=req.json.get("email"),
        is_admin=False,
        hash=bcrypt.generate_password_hash(pw.encode('utf-8')),
    )
    db.session.add(u)
    db.session.commit()
    return jsonify(u), 201


def admin_create_user(name, email, pw, admin=True):
    u = User(
        username=name,
        email=email,
        is_admin=admin,
        hash=bcrypt.generate_password_hash(pw.encode("utf-8")).decode("utf-8"),
    )
    db.session.add(u)
    return db.session.commit()