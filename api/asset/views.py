from flask import Blueprint

from .models import Asset, MeterReading

blueprint = Blueprint('asset', __name__)


@blueprint.route('/api/assets', methods=('GET',))
def list_assets():
    # return all assets as a list of json objects
    return [a.to_json() for a in Asset.query.all()], 200


@blueprint.route('/api/asset/<assetnum>', methods=['GET'])
def get_asset(assetnum):
    res = Asset.query.filter(Asset.num == assetnum).all()
    if len(res) == 0:
        return {'error': f"asset '{assetnum}' not found"}, 404
    elif len(res) != 1:
        return {'error': 'internal server error'}, 500
    return res[0].to_json(), 200


@blueprint.route('/api/asset', methods=['POST'])
def create_asset():
    # TODO handle post requests and insert an asset from json
    raise NotImplemented


@blueprint.route('/api/asset/<assetnum>/readings', methods=['GET'])
def asset_readings(assetnum):
    assets = Asset.query.filter(
        Asset.num == assetnum
    ).all()
    if len(assets) == 0:
        return {'error': f"asset '{assetnum}' not found"}, 404
    elif len(assets) > 1:
        return {'error': "internal server error"}, 500

    asset = assets[0].to_json()
    res = MeterReading.query.filter(
        MeterReading.assetnum == assetnum
    )
    readings, dates = [], []
    for r in res.all():
        readings.append(r.reading)
        dates.append(r.readingdate)
    asset['meter_readings'] = {'reading': readings, 'date': dates}
    return asset, 200
