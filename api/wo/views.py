from flask import Blueprint, request as req, jsonify
from sqlalchemy import func, distinct, column

from ..errors import Err, Ok
from ..extensions import db
from .models import WorkOrder

blueprint = Blueprint('work_order', __name__)


@blueprint.route('/api/workorders', methods=('GET',))
def list_workorders():
    search = req.args.get('search')
    if search:
        term = '|'.join(search.split(' '))
        # WARNING this will only work with postgres
        #   see db/postgres/text_search.sql
        res = WorkOrder.query.filter(
            column('search_vec').op('@@')(func.to_tsquery(term)))
    else:
        res = WorkOrder.query

    if 'asset_type' in req.args:
        res = res.filter_by(asset_type=req.args.get('asset_type'))
    if 'status' in req.args:
        res = res.filter_by(status=req.args.get('status'))
    res = res.order_by(WorkOrder.finish.desc())
    if 'limit' in req.args:
        res = res.limit(req.args.get('limit'))
    if 'offset' in req.args:
        res = res.offset(req.args.get('offset'))
    return {'workorders': res.all()}, 200


@blueprint.route('/api/workorder/statuses', methods=('GET',))
def workorder_statuses():
    return {
        'statuses': [
            s[0] for s in
            db.session.query(distinct(WorkOrder.status)).all()
        ]
    }


@blueprint.route('/api/workorder/<wonum>', methods=('GET', 'DELETE'))
def get_work_order(wonum):
    res = WorkOrder.query.filter_by(num=wonum)
    if req.method == 'GET':
        res = res.all()
        if len(res) != 1:
            return jsonify(Err(f"did not find {wonum}")), 404
        return jsonify(res[0])
    elif req.method == 'DELETE':
        ok = res.delete()
        if ok:
            return Ok(f'successfully deleted work order {wonum}')
        else:
            return Err(f'could not delete work order {wonum}', 404), 404

# @blueprint.route('/api/workorder', )