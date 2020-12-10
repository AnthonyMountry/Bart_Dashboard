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