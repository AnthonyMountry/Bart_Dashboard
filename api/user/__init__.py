from .views import blueprint, create_user
from .models import User
from ..extensions import db, bcrypt


def get_user(username: str):
    res = User.query.filter_by(username=username).all()
    if not res:
        return None
    elif len(res) != 1:
        return None
    return res[0]


def admin_create_user(name, email, pw, admin=True):
    u = User(
        username=name,
        email=email,
        is_admin=admin,
        hash=bcrypt.generate_password_hash(pw.encode("utf-8")).decode("utf-8"),
    )
    db.session.add(u)
    return db.session.commit()
