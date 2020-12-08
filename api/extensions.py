from flask_sqlalchemy import SQLAlchemy, Model
from flask_migrate import Migrate
from flask_compress import Compress
from flask_bcrypt import Bcrypt


class CrudModel(Model):

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

db = SQLAlchemy(model_class=CrudModel)
migrate = Migrate()
compress = Compress()
bcrypt = Bcrypt()
