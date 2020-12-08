from .views import blueprint
from .models import User

def get_user(username: str):
    res = User.query.filter_by(username=username).all()
    if not res:
        return None
    elif len(res) != 1:
        return None
    return res[0]