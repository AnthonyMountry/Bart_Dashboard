import flask.json
import traceback

from .errors import Error
from .asset.models import Asset, MeterReading
from .wo.models import WorkOrder


class ModelEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Error):
            return {
                'error': obj.msg,
                'debug': obj.__suppress_context__,
            }
        elif isinstance(obj, Asset):
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
        return super().default(obj)


def _json_exception(e: Exception, status_code=500):
    return {
        'error': 'internal server error',
        'debug': str(e),
        'type': type(e).__name__,
        'traceback': ''.join(traceback.format_tb(e.__traceback__)),
    }