from datetime import datetime
import pyexcel
from flask import Blueprint

from api.middleware import with_spreadsheet
from api.extensions import db

api = Blueprint('api', __name__)

@api.route('/api/test', methods=['GET', 'POST'])
def api_test(): # pragma no cover
    return {'testing': 'testing 123', 'date': datetime.now()}

@api.route('/api/upload', methods=('POST',))
@with_spreadsheet
def handle_data_uploads(book: pyexcel.Book):
    # TODO finish this
    # raise NotImplementedError
    return book.get_csv()



class MeterReadings: # (db.Model)
    project = db.Column(db.String(14), primary_key=True)
    department= db.Column(db.String(32))
    meter_name = db.Column(db.String(32))
    meter_description = db.Column(db.String(256))
    meter_reading = db.Column(db.Integer)
    reading_date = db.Column(db.String(32))
    meter_unit = db.Column(db.String(64))
    goal = db.Column(db.Integer)
    completion = db.Column(db.Float)
    goal_group = db.Column(db.String(64))
    work_order_num = db.Column(db.Integer)
    description = db.Column(db.String(256))
    cur_status = db.Column(db.String(32))
    reported_date = db.Column(db.String(32))
    location = db.Column(db.String(16))
    proj_type = db.Column(db.String(16))
    tpid = db.Column(db.Integer)
    ps_project = db.Column(db.String(16))
    ps_proj_description = db.Column(db.String(256))
    ps_activity = db.Column(db.String(16))
    ps_activity_description =db.Column(db.String(256))

# blueprint = Blueprint('_api', __name__)

#Start of Meter Reading API
#Meter list
# @blueprint.route('/api/MeterReadings', methods=['GET'])
# def ListMeterReadings():
#     if request.method == 'GET':
#         #get the list of MeterReadings
#         result = db.execute(
#             # TODO list the MeterReadings data
#             'select * from MeterReadings'
#         )
#         d = dict()
#         for MeterReadings in result:
#             d[MeterReadings[2]] = MeterReadings
#         return d

# #MPU Post Meter Reading (Not sure how to implement as many share same ID's, Project, etc)
# @blueprint.route('/api/MeterReadings/<project>', methods=['POST'])
# def post_MeterReadings(project):
#     raise NotImplemented

# #MPU get MeterReadings
# @blueprint.route('/api/MeterReadings/<project>', methods=['GET'])
# def get_MeterReadings(project):
#     raise NotImplemented

# #MPU Delete MeterReadings
# @blueprint.route('/api/MeterReadings/<project>', methods=['DELETE'])
# def del_MeterReadings(project):
#     raise NotImplemented

# #MPU Put MeterReadings
# @blueprint.route('/api/MeterReadings/<project>', methods=['PUT'])
# def put_MeterReadings(project):
#     raise NotImplemented
