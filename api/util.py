from flask import Response, jsonify
import flask.json
import traceback

from .errors import Err, Ok
from .asset.models import Asset, MeterReading
from .wo.models import WorkOrder
from .user.models import User
from .project.models import Mpu


class ModelEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Err):
            return obj.as_dict()
        if isinstance(obj, Asset):
            return obj.to_dict()
        elif isinstance(obj, MeterReading):
            return {
                'assetnum': obj.assetnum,
                'metername': obj.metername,
                'readingsource': obj.readingsource,
                'reading': obj.reading,
                'delta': obj.delta,
                'readingdate': obj.readingdate,
                'enterdate': obj.enterdate,
            }
        elif isinstance(obj, WorkOrder):
            return {
                'num': obj.num,
                'report_date': obj.report_date,
                'alias': obj.alias,
                'location': obj.location,
                'work_type': obj.work_type,
                'description': obj.description,
                'asset_type': obj.asset_type,
                'bartdept': obj.bartdept,
                'status': obj.status,
                'start': obj.start,
                'finish': obj.finish,
                'labor_hours': obj.labor_hours,
                'material_cost': obj.material_cost,
            }
        elif isinstance(obj, User):
            return {
                'username': obj.username,
                'email': obj.email,
                'is_admin': obj.is_admin,
            }
        elif isinstance(obj, Mpu):
            return {
                'id': obj.id,
                'name': obj.name,
                'short_name': obj.short_name,
                'ranking': obj.ranking,
                'description': obj.description,
                'location': obj.location,
                'sub_location': obj.sub_location,
                'district_location': obj.district_location,
                'mpu_phase': obj.mpu_phase,
                'budget_amount': obj.budget_amount,
                'expended_amount': obj.expended_amount,
                'remaining_budget': obj.remaining_budget,
                'funding_level': obj.funding_level,
                'end_date': obj.end_date,
                'rr_funded': obj.rr_funded,
                'monthly_burn_rate': obj.monthly_burn_rate,
                'accomplishments': obj.accomplishments,
                'project_group': obj.project_group,
                'project_manager': obj.project_manager,
                'program': obj.program,
                'review_format': obj.review_format,
            }
        return super().default(obj)


class ModelResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        print('running force_type')
        if isinstance(rv, (Ok, Err)):
            rv = jsonify(rv)
        return super(ModelResponse, cls).force_type(rv, environ)


def _json_exception(e: Exception, status_code=500):
    return {
        'error': 'internal server error',
        'debug': str(e),
        'type': type(e).__name__,
        'traceback': ''.join(traceback.format_tb(e.__traceback__)),
    }