from api.database import db

class WorkOrder(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date)
    alias = db.Column(db.String(24))
    location = db.Column(db.String(24))
    work_type = db.Column(db.String(8))
    description = db.Column(db.Text)
    asset_type = db.Column(db.String(32))
    bartdept = db.Column(db.String(32))
    status = db.Column(db.String(16))
    start = db.Column(db.Date)
    finish = db.Column(db.Date)
    labor_hours = db.Column(db.Float)
    material_cost = db.Column(db.Float)