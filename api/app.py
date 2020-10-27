import os
from flask import Flask, request, send_from_directory
import sqlite3

app = Flask(__name__, static_url_path='')

app.config['ENV'] = os.getenv('ENV') or 'dev' # dev is default
db = sqlite3.connect('db/dashboard.db')


@app.route('/', defaults={'path': None})
@app.route('/<path>', methods=['GET'])
def home(path):
    if not path:
        path = 'index.html'
    return send_from_directory('../public', path)


@app.route('/api/test', methods=['GET', 'POST'])
def api_test():
    r = request
    print(r.headers)
    if r.is_json:
        print('data:', r.get_json(force=True))
    else:
        print('this is not json:', r.data)
    print(r.files)
    return {'key': 'value'}


@app.route('/api/upload<filename>', methods=['POST'])
def handle_uploads(filename):
    if 'file' not in request.files:
        # TODO send back an error
        pass
    f = request.files['file']
    if not f.filename:
        # TODO send back an error
        pass
    if not f.filename.endswith('.xlsx') or not f.filename.endswith('.csv'):
        # TODO send back an error
        pass
    # now do stuff with the file
    f.save(filename)
    # or read the file into a db or whatever


@app.route('/api/asset/<assetnum>', methods=['GET', 'POST'])
def asset(assetnum):
    # TODO finish these sql queries
    if request.method == 'GET':
        # get the asset and set it back
        result = db.execute(
            '''
            SELECT *
            FROM assets_table
            WHERE
                assetnum = ?''',
            (assetnum, ),
        )
        return result
    else:
        # insert the new asset into the db
        db.execute(
            '''
            INSERT INTO assets_table
            ... whatever the rest of this query is...''',
            (assetnum, ),
        )
