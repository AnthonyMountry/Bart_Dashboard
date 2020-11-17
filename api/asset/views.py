from flask import Blueprint, jsonify, request

from .models import Asset, MeterReading

blueprint = Blueprint('asset', __name__)


@blueprint.route('/api/assets', methods=['GET'])
def list_assets():
    # Return all assets as a list of json objects
    return {
        'assets': Asset.query.limit(
            request.args.get('limit')
        ).offset(
            request.args.get('offset')
        ).all()
    }, 200


@blueprint.route('/api/asset/<assetnum>', methods=['GET'])
def get_asset(assetnum):
    res = Asset.query.filter_by(num=assetnum).all()
    if len(res) == 0:
        return {'error': f"asset '{assetnum}' not found"}, 404
    elif len(res) != 1:
        return {'error': 'internal server error'}, 500
    return jsonify(res[0]), 200


@blueprint.route('/api/asset', methods=['POST'])
def create_asset():
    # TODO handle post requests and insert an asset from json
    raise NotImplementedError


@blueprint.route('/api/asset/<assetnum>', methods=('PUT',))
def update_asset(assetnum):
    # TODO Update the asset where assetnum=assetnum
    raise NotImplementedError


@blueprint.route('/api/asset/<assetnum>', methods=('DELETE',))
def delete_asset(assetnum):
    # TODO delete the asset
    raise NotImplementedError


@blueprint.route('/api/asset/<assetnum>/readings', methods=['GET'])
def asset_readings(assetnum):
    assets = Asset.query.filter(
        Asset.num == assetnum
    ).all()
    if len(assets) == 0:
        return {'error': f"asset '{assetnum}' not found"}, 404
    elif len(assets) > 1:
        return {'error': "internal server error"}, 500

    asset = assets[0].to_dict()
    res = MeterReading.query.filter_by(assetnum=assetnum) \
        .limit(request.args.get('limit')) \
        .offset(request.args.get('offset'))
    readings, dates = [], []
    for r in res.all():
        readings.append(r.reading)
        dates.append(r.readingdate)

    asset['meter_readings'] = [{'reading': r, 'date': b} for r, b in zip(readings, dates)]
    return asset, 200
