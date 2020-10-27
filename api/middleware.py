import os
from functools import wraps
from flask import request

valid_file_exts = {'xlsx', 'xls', 'csv'}

def spreadsheet_required(handler):
    """Checks that the file-upload request has a spreadsheet

    Usage
    ----
    @app.route('/some/api/route')
    @spreadsheet_required
    def endpoint_handler():
        f = request.file['file']
        # process spreadsheet
        return
    """
    @wraps(handler)
    def inner(*args, **kwargs):
        if 'file' not in request.files:
            return (
                {"error", "internal server error"},  # response body
                500,                                 # status code
                {'Content-Type': 'application/json'} # response headers
            )
        f = request.files['file']
        if not f.filename:
            return {'error': 'no file name given'}, 500

        _, ext = os.path.splitext(f.filename)
        if ext not in valid_file_exts:
            return {'error': 'invalid file type'}
        return handler(*args, **kwargs)
    return inner
