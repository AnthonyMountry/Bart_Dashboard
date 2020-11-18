from os.path import (
    join as path_join,
    exists as path_exists,
)
import traceback

import pyexcel
from flask import (
    Blueprint,
    request,
    send_from_directory,
    current_app,
)
from werkzeug.exceptions import NotFound

from api.middleware import with_spreadsheet
from api.database import db

blueprint = Blueprint('api', __name__)

STATIC_DIR = 'public'

def static(folder):
    base = STATIC_DIR
    target = path_join(base, folder)
    def fn(file):
        if path_exists(path_join('public', folder, file)):
            return send_from_directory(target, file)
        else:
            return send_from_directory(base, file)
    blueprint.add_url_rule(
        path_join('/', folder, '<file>'),
        'static_'+folder,
        fn,
        methods=['GET']
    )

static('css')
static('html')
static('js')
static('img')

@blueprint.route('/', defaults={'path': None})
@blueprint.route('/<path>', methods=['GET'])
def home(path):
    '''
    return the home page and any other public files
    '''
    if not path:
        path = 'html/index.html'
    return send_from_directory(STATIC_DIR, path)


@blueprint.route('/analytics', methods=['GET'])
def analytics():
    return send_from_directory(STATIC_DIR, 'html/Analytics.html')

@blueprint.route('/reports', methods=['GET'])
def reports():
    return send_from_directory(STATIC_DIR, 'html/Reports.html')


@blueprint.errorhandler(Exception)
def handle_all_errors(err):
    with current_app.app_context():
        debug = current_app.config.get('DEBUG')
    resp = {
        'error': str(err),
        'type': type(err).__name__,
    }
    tb = ''.join(traceback.format_tb(err.__traceback__))
    if debug:
        resp['traceback'] = tb
    print(tb, end='')
    print(err)
    return resp, 500

@blueprint.errorhandler(NotFound)
def handle_status_notfound(err):
    tb = traceback.format_tb(err.__traceback__)
    headers = dict(err.get_headers())
    print(''.join(tb))
    print(err)
    print(dir(err))
    data = {
        'error': err,
        'type': type(err).__name__,
        'traceback': tb,
    }
    if 'text/html' in headers['Content-Type']:
        nl = "\n"
        return f'''
<h1>404</h1>
<h2>Sorry, we couldn'd find this page.</h2>
<p style="color:red;">{err.description}</p>
    <div style="background-color: lightgrey">
        {''.join('<a>' + t.replace(nl, "<br>") + '</a>' for t in tb) }
    </div>
<br>
<p>It was probably the backend guys breaking something 😉.</p>
''', 404
    else:
        return {
            'error': str(err),
            'type': type(err).__name__,
        }, 404

@blueprint.errorhandler(NotImplementedError)
def not_impl_handler(e):
    tb = traceback.extract_tb(e.__traceback__)
    last = tb[-1]
    path = last.name
    for r in current_app.url_map.iter_rules():
        if r.endpoint == last.name:
            path = r.rule
            break
    return {
        'error': f"Endpoint '{path}' not implemented",
        'type': type(e).__name__,
        'debug': f"File '{last.filename}', line {last.lineno}",
    }, 501

@blueprint.route('/api/rootpath', methods=['GET'])
def _get_rootpath():
    return current_app.root_path

@blueprint.route('/api/test', methods=['GET', 'POST'])
def api_test():
    # return {'db': repr(db), 'app': repr(current_app)}
    # raise NotImplementedError
    return {'testing': 'testing 123'}


@blueprint.route('/api/upload', methods=('POST',))
@with_spreadsheet
def handle_data_uploads(book: pyexcel.Book):
    # TODO finish this
    raise NotImplementedError


class Mpu(db.Model):
    id = db.Column(db.String(14), primary_key=True)
    name = db.Column(db.String(128))
    short_name = db.Column(db.String(128))
    ranking = db.Column(db.Integer)
    description = db.Column(db.String(512))
    location = db.Column(db.String(32))
    sub_location = db.Column(db.String(32))
    district_location = db.Column(db.String(64))
    mpu_phase = db.Column(db.String(32))
    budget_amount = db.Column(db.Float)
    expended_amount = db.Column(db.Float)
    monthly_burn_rate = db.Column(db.Float)
    remaining_budget = db.Column(db.Float)
    funding_level = db.Column(db.String(16))
    rr_funded = db.Column(db.Boolean)
    project_group = db.Column(db.String(64))
    project_manager = db.Column(db.String(32))
    accomplishments = db.Column(db.String(128))
    program = db.Column(db.String(32))
    review_format = db.Column(db.String(32))
    end_date = db.Column(db.Date)


class MeterReadings(db.Model):
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

#Workorder API

#MPU Post Workorder
@blueprint.route('/api/workorder/<id>', methods=['POST'])
def post_workorder(id):
    raise NotImplementedError

#MPU get Workorder
@blueprint.route('/api/workorder/<id>', methods=['GET'])
def get_workorder(id):
    raise NotImplementedError

#MPU Delete Workorder
@blueprint.route('/api/workorder/<id>', methods=['DELETE'])
def del_workorder(id):
    raise NotImplementedError

#MPU Put Workorder
@blueprint.route('/api/workorder/<id>', methods=['PUT'])
def put_workorder(id):
    raise NotImplementedError

# Start of MPU API
#MPU
#MPU list
@blueprint.route('/api/mpus', methods=['GET'])
def listMPU():
    return {
        'mpus': Mpu.query.limit(
            request.args.get('limit')
        ).all()
    }, 200


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
@blueprint.route('/api/MeterReadings', methods=['GET'])
def ListMeterReadings():
    if request.method == 'GET':
        #get the list of MeterReadings
        result = db.execute(
            # TODO list the MeterReadings data
            'select * from MeterReadings'
        )
        d = dict()
        for MeterReadings in result:
            d[MeterReadings[2]] = MeterReadings
        return d

#MPU Post Meter Reading (Not sure how to implement as many share same ID's, Project, etc)
@blueprint.route('/api/MeterReadings/<project>', methods=['POST'])
def post_MeterReadings(project):
    raise NotImplemented

#MPU get MeterReadings
@blueprint.route('/api/MeterReadings/<project>', methods=['GET'])
def get_MeterReadings(project):
    raise NotImplemented

#MPU Delete MeterReadings
@blueprint.route('/api/MeterReadings/<project>', methods=['DELETE'])
def del_MeterReadings(project):
    raise NotImplemented

#MPU Put MeterReadings
@blueprint.route('/api/MeterReadings/<project>', methods=['PUT'])
def put_MeterReadings(project):
    raise NotImplemented
