from flask import current_app
import traceback


class Error(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg

    def as_dict(self):
        return {
            'error': self.msg,
            'status': 500 if len(self.args) <= 1 else self.args[1]
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
        nl = "\n"
        return f'''
<h1>404</h1>
<h2>Sorry, we couldn'd find this page.</h2>
<p style="color:red;">{err.description}</p>
    <div style="background-color: lightgrey">
        {''.join('<a>' + t.replace(nl, "<br>") + '</a>' for t in tb) }
    </div>
<br>
<p>It was probably the backend guys breaking something 😉.</p>
''', 404
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
