import os
from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

app.config['ENV'] = os.getenv('ENV') or 'dev' # dev is default
db = sqlite3.connect('db/dashboard.db')


@app.route('/')
def home():
    # TODO return the actual homepage
    return '<h1>insert graph here lol</h1>'


@app.route('/api/test', methods=['GET', 'POST'])
def api_test():
    r = request
    # print(dir(request))
    # print()

    print(r.headers)
    if r.is_json:
        print('data:', r.get_json(force=True))
    else:
        print('this is not json:', r.data)
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
        db.exectute(
            '''
            INSERT INTO assets_table
            ... whatever the rest of this query is...''',
            (assetnum, ),
        )

