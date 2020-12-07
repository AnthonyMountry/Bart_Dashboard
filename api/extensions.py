from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_compress import Compress

db = SQLAlchemy()
migrate = Migrate()
compress = Compress()