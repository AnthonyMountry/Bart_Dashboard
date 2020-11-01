import os
import sqlite3
import traceback

import pyexcel
from flask import (
    Flask,
    request,
    send_from_directory,
)

app = Flask(__name__)

app.config['ENV'] = os.getenv('ENV') or 'dev' # dev is default
db = sqlite3.connect('db/dashboard.db')

DEBUG = True

VALID_CONTENT_TYPES = {
    "application/vnd.ms-excel",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.ms-excel.template.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "text/csv",
}


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


@app.route('/api/upload', methods=['POST'])
def handle_uploads():
    '''handle_uploads handles the spreadsheet file uploads'''
    f = request.files['file']
    if f.content_type not in VALID_CONTENT_TYPES:
        return {"error": "Unknown content type"}, 400
    if not f.filename:
        return {"error": "No filename"}
    ext = f.filename.split('.')[-1]
    book = pyexcel.get_book(file_type=ext, file_content=f.read())
    # TODO do stuff with sheet
    return {'success': f'{f.filename} uploaded successfully'}, 200 # status "ok"


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


def _json_exception(e: Exception, status_code=500):
    if DEBUG:
        return {
            'error': 'internal server error',
            'debug': str(e),
            'type': type(e).__name__,
            'traceback': ''.join(traceback.format_tb(e.__traceback__)),
        }
    else:
        return {
            'error': 'internal server error',
            'statuscode': status_code,
        }

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)