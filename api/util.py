import traceback

from .asset.models import Asset, MeterReading
import flask.json


class ModelEncoder(flask.json.JSONEncoder):
    def default(self, obj):
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
        return super().default(obj)


def _json_exception(e: Exception, status_code=500):
    return {
        'error': 'internal server error',
        'debug': str(e),
        'type': type(e).__name__,
        'traceback': ''.join(traceback.format_tb(e.__traceback__)),
    }