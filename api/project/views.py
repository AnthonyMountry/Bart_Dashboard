from flask import Blueprint, request as req
from sqlalchemy import func, column
from .models import Mpu, ProjectMeter

blueprint = Blueprint('mpu', __name__)

@blueprint.route('/api/mpus', methods=['GET'])
def list_mpu():
    search = req.args.get('search')
    if search:
        term = '|'.join(search.split(' '))
        res = Mpu.query.filter(
            func.to_tsvector(
                Mpu.name.op('||')(' ')                       \
                .op('||')(Mpu.short_name).op('||')(' ')      \
                .op('||')(Mpu.description).op('||')(' ')     \
                .op('||')(Mpu.location).op('||')(' ')        \
                .op('||')(Mpu.sub_location).op('||')(' ')    \
                .op('||')(Mpu.project_group).op('||')(' ')   \
                .op('||')(
                    func.coalesce(Mpu.accomplishments, '')
                ).op('||')(' ') \
                .op('||')(Mpu.project_manager)
            ).op('@@')(func.to_tsquery(term)),
        )
        # res = Mpu.query.filter(column('searc'))
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