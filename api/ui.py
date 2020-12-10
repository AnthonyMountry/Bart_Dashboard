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

from .user import get_user

blueprint = Blueprint('ui', __name__)

STATIC_DIR = 'public'

def newstatic(folder):
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


# newstatic('css')
# newstatic('img')
# newstatic('js')
# newstatic('html')


@blueprint.route('/', defaults={'path': None})
@blueprint.route('/<path>', methods=['GET', 'POST'])
def home(path):
    '''
    return the home page and any other public files
    '''
    if not path:
        path = 'html/index.html'
    return send_from_directory(STATIC_DIR, path)


@blueprint.route('/login', methods=set(['GET', 'POST']))
def login():
    if request.method == 'GET':
        return render_template("login.html")
    us = request.form.get("username")
    pw = request.form.get('password') or request.form.get("pw")

    if not us or not pw:
        return send_from_directory(STATIC_DIR, "html/bad_auth.html")
    u = get_user(us)
    if u is None:
        return render_template("login.html", bad_login=True)
    if not u.password_ok(pw):
        return render_template("login.html", bad_login=True, bad_password=True)
    return redirect("/dashboard")


@blueprint.route('/dashboard', methods=("GET",))
def dashboard():
    return send_from_directory(STATIC_DIR, "html/dash.html")


@blueprint.route('/search', methods=("GET", "POST"))
def search():
    search_term = request.args.get('search') or request.args.get('q') or ''
    return render_template("search.html",
        page_title='Search',
        host=request.host_url,
        search_term=search_term,
    )


@blueprint.route('/analytics', methods=['GET'])
def analytics():
    return render_template("analytics.html",
        page_title='Analytics',
        host=request.host_url,
    )


@blueprint.route('/notifications', methods=("GET",))
def notifications():
    return render_template("notifications.html",
        page_title='Notifacations',
    )


@blueprint.route('/reports', methods=['GET'])
def reports():
    return send_from_directory(STATIC_DIR, 'html/Reports.html')


@blueprint.route('/asset', methods=('GET', ))
def route_template():
    num = request.args.get('assetnum')
    return render_template("asset.html",
        asset_num=num,
        page_title=f'Asset {num}',
        host=request.host_url,
    )
