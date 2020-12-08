from api.extensions import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    hash = db.Column(db.String(128))

    def password_ok(self, pw) -> bool:
        if pw is None:
            return False
        return bcrypt.check_password_hash(self.hash, pw.encode('utf-8'))
