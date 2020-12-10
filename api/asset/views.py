from flask import Blueprint, jsonify, request
from sqlalchemy import func, column

from ..errors import Ok
from .models import Asset, MeterReading
from ..extensions import db

blueprint = Blueprint('asset', __name__)

@blueprint.route('/api/assets', methods=['GET'])
def list_assets():
    search = request.args.get("search")
    if search:
        term = '|'.join(search.split(' '))
        # WARNING this will only work with postgres
        #   see db/postgres/text_search.sql
        res = Asset.query.filter(
            column('search_vec').op('@@')(func.to_tsquery(term)))
    else:
        res = Asset.query

    limit = request.args.get("limit")
    offset = request.args.get('offset')
    if limit:
        res  = res.limit(limit)
    if offset:
        res = res.offset(offset)

    return Ok(
        msg='assets successfully listed',
        assets=res.all(),
    )

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
    assets = Asset.query.filter_by(num=assetnum).all()

    if len(assets) == 0:
        return {'error': f"asset '{assetnum}' not found"}, 404
    if len(assets) > 1:
        return {'error': "internal server error"}, 500
    asset = assets[0].to_dict()

    res = MeterReading.query.filter_by(assetnum=assetnum) \
        .limit(request.args.get('limit')) \
        .offset(request.args.get('offset'))
    asset['meter_readings'] = res.all();
    return asset, 200
