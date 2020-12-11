from flask import Blueprint, request as req
from sqlalchemy import func, column
from .models import Mpu, ProjectMeter

blueprint = Blueprint('mpu', __name__)

@blueprint.route('/api/mpus', methods=['GET'])
def list_mpu():
    search = req.args.get('search')
    if search:
        term = '|'.join(search.split(' '))
        # WARNING this will only work with postgres
        #   see db/postgres/text_search.sql
        res = Mpu.query.filter(
            column('search_vec').op('@@')(func.to_tsquery(term)))
    else:
        res = Mpu.query

    if 'limit' in req.args:
        res = res.limit(req.args.get('limit'))
    if 'offset' in req.args:
        res = res.offset(req.args.get('offset'))
    return {
        'mpus': res.all()
    }, 200

@blueprint.route('/api/mpu', methods=('POST',))
def create_mpu():
    pass


#Delete MPU by IDs
@blueprint.route('/api/mpu/<id>', methods=('DELETE', 'PUT', 'GET'))
def del_mpu(id):
    raise NotImplementedError


#MPU PUT IDs
#MPU Milestones API
#MPU Post Milestones
@blueprint.route('/api/mpu/<id>/milestone', methods=('POST', 'GET', 'DELETE', 'PUT'))
def post_mpu_milestone(id):
    raise NotImplementedError


#MPU Funds API
#MPU Post Funds
@blueprint.route('/api/mpu/<id>/fund', methods=('POST', 'GET', 'DELETE' 'PUT'))
def post_mpu_fund(id):
    raise NotImplementedError


#MPU Criteria API
#MPU Post Criteria
@blueprint.route('/api/mpu/<id>/criteria', methods=('POST', 'GET', 'DELETE', 'PUT'))
def post_mpu_criteria(id):
    raise NotImplementedError