from datetime import datetime
import pyexcel
from flask import (
    Blueprint,
    request,
    current_app,
)

from api.middleware import with_spreadsheet
from api.extensions import db


api = Blueprint('api', __name__)
STATIC_DIR = 'public'

@api.route('/api/rootpath', methods=['GET'])
def _get_rootpath():
    return current_app.root_path

@api.route('/api/test', methods=['GET', 'POST'])
def api_test():
    print(request.form)
    print(request.json)
    print(request.get_json())
    print(request.json.get('test'))
    print(request.json.get('name'))
    return {'testing': 'testing 123', 'date': datetime.now()}

@api.route('/api/upload', methods=('POST',))
@with_spreadsheet
def handle_data_uploads(book: pyexcel.Book):
    # TODO finish this
    # raise NotImplementedError
    return book.get_csv()


blueprint = Blueprint('_api', __name__)
# class ProjectMeter(db.Model): pass


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


#MPU IDs
#MPU post IDs
@blueprint.route('/api/mpu', methods=['POST'])
def create_new_mpu():
    # insert the new asset into the db
    result = db.execute(
        '''
        INSERT INTO mpu
        ... whatever the rest of this query is...''',
        (id, ),
    )


#MPU get IDs
@blueprint.route('/api/mpu/<id>', methods=['GET'])
def get_mpu(id):
    #get MPUS with ID
    result = db.execute(
       '''
        SELECT *
        FROM mpu
        WHERE
            id = ?''',
        (id, ),
    )
    return result

#Delete MPU by IDs
@blueprint.route('/api/mpu/<id>', methods=['DELETE'])
def del_mpu(id):
    #Delete ID
    result = db.execute(
        #TODO remove ID
    )

#MPU PUT IDs
@blueprint.route('/api/mpu/<id>', methods=['PUT'])
def put_mpu(id):
    #Put MPUs
        result = db.execute(
        #TODO PUT ID
    )

#MPU Milestones API
#MPU Post Milestones
@blueprint.route('/api/mpu/<id>/milestone', methods=['POST'])
def post_mpu_milestone(id):
    raise NotImplementedError

#MPU get Milestones
@blueprint.route('/api/mpu/<id>/milestone', methods=['GET'])
def get_mpu_milestone(id):
    raise NotImplementedError

#MPU Delete Milestones
@blueprint.route('/api/mpu/<id>/milestone', methods=['DELETE'])
def del_mpu_milestone(id):
    raise NotImplementedError

#MPU Put Milestones
@blueprint.route('/api/mpu/<id>/milestone', methods=['PUT'])
def put_mpu_milestone(id):
    raise NotImplementedError

#MPU Funds API
#MPU Post Funds
@blueprint.route('/api/mpu/<id>/fund', methods=['POST'])
def post_mpu_fund(id):
    raise NotImplementedError

#MPU get Funds
@blueprint.route('/api/mpu/<id>/fund', methods=['GET'])
def get_mpu_fund(id):
    raise NotImplementedError

#MPU Delete Funds
@blueprint.route('/api/mpu/<id>/fund', methods=['DELETE'])
def del_mpu_fund(id):
    raise NotImplementedError

#MPU Put Funds
@blueprint.route('/api/mpu/<id>/fund', methods=['PUT'])
def put_mpu_fund(id):
    raise NotImplementedError

#MPU Criteria API
#MPU Post Criteria
@blueprint.route('/api/mpu/<id>/criteria', methods=['POST'])
def post_mpu_criteria(id):
    raise NotImplementedError

#MPU get Criteria
@blueprint.route('/api/mpu/<id>/criteria', methods=['GET'])
def get_mpu_criteria(id):
    raise NotImplementedError

#MPU Delete Criteria
@blueprint.route('/api/mpu/<id>/criteria', methods=['DELETE'])
def del_mpu_criteria(id):
    raise NotImplementedError

#MPU Put Criteria
@blueprint.route('/api/mpu/<id>/criteria', methods=['PUT'])
def put_mpu_criteria(id):
    raise NotImplementedError

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
