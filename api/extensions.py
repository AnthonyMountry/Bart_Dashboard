from flask_sqlalchemy import SQLAlchemy, Model
from flask_migrate import Migrate
from flask_compress import Compress
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
compress = Compress()
bcrypt = Bcrypt()
