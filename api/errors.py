from flask import current_app, Response
import traceback

from flask.templating import render_template


def Ok(msg, **data):
    resp = {
        'success': msg,
        'status': 200,
    }
    resp.update(data)
    return resp, 200


class Err(Exception):
    msg: str

    def __init__(self, msg: str):
        self.tb = traceback.format_tb(self.__traceback__)
        self.msg = msg

    def as_dict(self):
        if len(self.args) <= 1:
            code = 500
        else:
            code = self.args[1]
        return {
            'error': self.msg,
            'code': code,
            'debug': ''.join(self.tb)
        }


def handle_all(err):
    with current_app.app_context():
        debug = current_app.config.get('DEBUG')
    resp = {
        'error': str(err),
        'type': type(err).__name__,
    }
    tb = ''.join(traceback.format_tb(err.__traceback__))
    if debug:
        resp['traceback'] = tb
    print(tb, end='')
    print(err)
    return resp, 500


def handle_notfound(err):
    tb = traceback.format_tb(err.__traceback__)
    headers = dict(err.get_headers())
    print(''.join(tb))
    print(err)
    if 'text/html' in headers['Content-Type']:
        return render_template("404.html",
            traceback=tb,
            error=str(err),
        ), 404
    else:
        return {
            'error': str(err),
            'type': type(err).__name__,
        }, 404


def handle_not_impl(e):
    tb = traceback.extract_tb(e.__traceback__)
    last = tb[-1]
    path = last.name
    for r in current_app.url_map.iter_rules():
        if r.endpoint == last.name:
            path = r.rule
            break
    return {
        'error': f"Endpoint '{path}' not implemented",
        'type': type(e).__name__,
        'debug': f"File '{last.filename}', line {last.lineno}",
    }, 501
