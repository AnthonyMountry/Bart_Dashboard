import os
from functools import wraps
from flask import request

VALID_FILE_EXTS = {'xlsx', 'xlsm', 'xltm', 'xls', 'csv'}

VALID_CONTENT_TYPES = {
    "application/vnd.ms-excel",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.ms-excel.template.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "text/csv",
}

def spreadsheet_upload(handler):
    """Checks that the file-upload request has a spreadsheet

    Usage
    ----
    @app.route('/some/api/route')
    @spreadsheet_required
    def endpoint_handler():
        # process data
        return
    """
    @wraps(handler)
    def inner(*args, **kwargs):
        content_type = request.headers.get('Content-Type')
        data_type = request.args.get('type')
        filename = request.args.get('filename')

        if content_type not in VALID_CONTENT_TYPES:
            return _error("Unknown content type")
        elif not filename:
            return _error("No filename given")
        elif not data_type:
            return _error("No type for this spreadsheet")
        return handler(*args, **kwargs)
    return inner


def _error(msg, status_code=400):
    return {"error": msg}, status_code
