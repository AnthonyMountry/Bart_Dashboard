from flask import Blueprint, request, jsonify

from ..errors import Err, Ok
from .models import WorkOrder


blueprint = Blueprint('work_order', __name__)


@blueprint.route('/api/workorders', methods=('GET',))
def list_workorders():
    return {
        'workorders': WorkOrder.query           \
            .limit(request.args.get("limit"))   \
            .offset(request.args.get("offset")) \
            .all()
    }, 200


@blueprint.route('/api/workorder/<wonum>', methods=('GET', 'DELETE'))
def get_work_order(wonum):
    res = WorkOrder.query.filter_by(num=wonum)
    if request.method == 'GET':
        res = res.all()
        if len(res) != 1:
            return jsonify(Err(f"did not find {wonum}")), 404
        return jsonify(res[0])
    elif request.method == 'DELETE':
        ok = res.delete()
        if ok:
            return Ok(f'successfully deleted work order {wonum}')
        else:
            return Err(f'could not delete work order {wonum}', 404), 404
