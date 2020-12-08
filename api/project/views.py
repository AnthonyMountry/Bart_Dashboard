from flask import Blueprint, request
from .models import Mpu, ProjectMeter

blueprint = Blueprint('mpu', __name__)

@blueprint.route('/api/mpus', methods=['GET'])
def list_mpu():
    return {
        'mpus': Mpu.query.limit(
            request.args.get('limit')
        ).all()
    }, 200

@blueprint.route('/api/mpu', methods=('POST',))
def create_mpu():
    pass