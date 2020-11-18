from flask import Blueprint, request, jsonify

from .models import WorkOrder

blueprint = Blueprint('work_order', __name__)

@blueprint.route('/api/workorders', methods=('GET',))
def list_workorders():
    return {
        'workorders': WorkOrder.query \
            .limit(request.args.get("limit")) \
            .offset(request.args.get("offset")) \
            .all()
    }, 200

@blueprint.route('/api/workorder/<wonum>', methods=('GET',))
def get_work_order(wonum):
    res = WorkOrder.query.filter_by(num=wonum).all()
    if len(res) != 1:
        # TODO error
        ...
    return jsonify(res[0])
