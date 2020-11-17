from ..app import db

STATUS_DECOMMISSIONED = 'DECOMMISSIONED'
STATUS_OPERATING = 'OPERATING'


class Asset(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    bartdept = db.Column(db.String(8))
    description = db.Column(db.String(128))
    status = db.Column(db.String(16))

    def to_dict(self):
        return {
            'num': self.num,
            'bartdept': self.bartdept,
            'description': self.description,
            'status': self.status,
        }


class MeterReading(db.Model):
    # Sorry about all the primary keys, I needed to get around
    # some SQLAlchemy-specific limitations.
    assetnum = db.Column(db.Integer, primary_key=True)
    metername = db.Column(db.String(16), primary_key=True)
    readingsource = db.Column(db.String(32), primary_key=True)
    reading = db.Column(db.Integer, primary_key=True, nullable=False)
    delta = db.Column(db.Integer, primary_key=True)
    readingdate = db.Column(db.Date, primary_key=True)
    enterdate = db.Column(db.Date, primary_key=True)
