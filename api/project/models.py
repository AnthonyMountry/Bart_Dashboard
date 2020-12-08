from api.extensions import db

class Mpu(db.Model):
    id          = db.Column(db.String(14), primary_key=True)
    name        = db.Column(db.String(128))
    short_name  = db.Column(db.String(128))
    ranking     = db.Column(db.Integer)
    description = db.Column(db.Text)
    location    = db.Column(db.String(128))
    sub_location = db.Column(db.String(128))
    district_location = db.Column(db.String(32))
    mpu_phase = db.Column(db.String(32))
    budget_amount    = db.Column(db.Float)
    expended_amount  = db.Column(db.Float)
    remaining_budget = db.Column(db.Float)
    funding_level    = db.Column(db.String(16))
    end_date = db.Column(db.Date)
    rr_funded = db.Column(db.Boolean)
    monthly_burn_rate = db.Column(db.Float)
    accomplishments = db.Column(db.Text)
    project_group = db.Column(db.String(50))
    project_manager = db.Column(db.Text)
    program = db.Column(db.String(32))
    review_format = db.Column(db.String(24))

class ProjectMeter(db.Model):
    project                  = db.Column(db.String(3))
    department               = db.Column(db.String(20))
    meter_location           = db.Column(db.String(8))
    metername                = db.Column(db.String(10))
    meter_description        = db.Column(db.String(128))
    meter_reading            = db.Column(db.Integer, default=0)
    reading_date             = db.Column(db.Date)
    meter_units_sql          = db.Column(db.String(4))
    meter_units_from_project = db.Column(db.String(22))
    meter_units              = db.Column(db.String(22))
    goal                     = db.Column(db.Integer)
    completion_percent       = db.Column(db.String(8)) # TODO remove this
    goal_group               = db.Column(db.String(32))
    workorder_num            = db.Column(db.Integer, primary_key=True)
    description              = db.Column(db.String(128))
    current_status           = db.Column(db.String(20))
    reported_date            = db.Column(db.Date)
    type                     = db.Column(db.Text)
    tpid                     = db.Column(db.Integer, primary_key=True)
    ps_project               = db.Column(db.Text)
    ps_project_description   = db.Column(db.Text)
    ps_activity              = db.Column(db.Text)
    ps_activity_description  = db.Column(db.Text)
