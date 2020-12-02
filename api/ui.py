from os.path import (
    join as path_join,
    exists as path_exists,
)

from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    send_from_directory,
)

blueprint = Blueprint('ui', __name__)

STATIC_DIR = 'public'

def static(folder):
    base = STATIC_DIR
    target = path_join(base, folder)
    def fn(file):
        if path_exists(path_join('public', folder, file)):
            return send_from_directory(target, file)
        else:
            return send_from_directory(base, file)
    blueprint.add_url_rule(
        path_join('/', folder, '<file>'),
        'static_'+folder,
        fn,
        methods=['GET']
    )

static('css')
static('img')
static('js')
static('html')

@blueprint.route('/', defaults={'path': None})
@blueprint.route('/<path>', methods=['GET', 'POST'])
def home(path):
    '''
    return the home page and any other public files
    '''
    if not path:
        path = 'html/index.html'
    return send_from_directory(STATIC_DIR, path)

@blueprint.route('/dashboard', methods=("GET",))
def dashboard():
    return send_from_directory(STATIC_DIR, "html/dash.html")

@blueprint.route('/search', methods=("GET",))
def search():
    return send_from_directory(STATIC_DIR, "html/search.html")

@blueprint.route('/analytics', methods=['GET'])
def analytics():
    return send_from_directory(STATIC_DIR, 'html/Analytics.html')
    # return render_template("analytics.html",
    #     page_title=f'Dashboard',
    #     host=request.host_url,
    # )

@blueprint.route('/reports', methods=['GET'])
def reports():
    return send_from_directory(STATIC_DIR, 'html/Reports.html')


@blueprint.route('/login', methods=set(['GET', 'POST']))
def login():
    if request.method == 'GET':
        return send_from_directory(STATIC_DIR, 'html/index.html')
    # TODO handle auth
    if request.method != "POST":
        return '''<h1>i dont know whats going on</h1>'''

    us = request.form.get("username")
    pw = request.form.get('password') or request.form.get("pw")
    if not us or not pw:
        return send_from_directory(STATIC_DIR, "html/bad_auth.html")
    return redirect("/dashboard")


@blueprint.route('/asset', methods=('GET', ))
def route_template():
    num = request.args.get('assetnum')
    return render_template("asset.html",
        asset_num=num,
        page_title=f'Asset {num}',
        host=request.host_url,
    )

@blueprint.route('/_dashboard', methods=("GET",))
def _dashboard_route():
    return render_template("dashboard.html",
        page_title=f'Dashboard',
        host=request.host_url,
    )

@blueprint.route('/_analytics', methods=['GET'])
def _analytics():
    # return send_from_directory(STATIC_DIR, 'html/Analytics.html')
    return render_template("analytics.html",
        page_title=f'Dashboard',
        host=request.host_url,
    )