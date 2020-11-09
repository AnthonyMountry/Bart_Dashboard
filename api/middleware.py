from functools import wraps
from flask import request

import pyexcel

VALID_FILE_EXTS = {'xlsx', 'xlsm', 'xltm', 'xls', 'csv'}

VALID_CONTENT_TYPES = {
    "application/vnd.ms-excel",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.ms-excel.template.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "text/csv",
}


def with_spreadsheet(handler):
    """Run write an endpoint that will accept
       an excel book as an argument.

    Usage
    -----
    @app.route('/some/api/route')
    @with_spreadsheet
    def endpoint_handler(book: pyexcel.Book):
        # process data in book
        return {"msg": "ok"}
    """
    @wraps(handler)
    def inner(*args, **kwargs):
        # if request.headers.get('Content-Type') != 'multipart/form-data':
        #     return {'error': "bad content type, expected 'multipart/form-data'"}, 400
        if 'file' not in request.files:
            return {'error': 'no file'}, 400
        f = request.files['file']
        if f.content_type not in VALID_CONTENT_TYPES:
            return {"error": "Unknown content type"}, 400
        if not f.filename:
            return {"error": "No filename"}, 400
        ext = f.filename.split('.')[-1]
        book = pyexcel.get_book(file_type=ext, file_content=f.read())
        book.filename = f.filename
        return handler(book, *args, **kwargs)
    return inner


def _error(msg, status_code=400):
    return {"error": msg}, status_code
