from flask import (
    session,
    redirect,
    url_for,
    request,
    g,
    flash,
    abort,
)
from models.user import User
from models.topic import Topic
from models.reply import Reply
from functools import wraps


def current_user():
    """
    返回当前用户，未登录返回 None
    """
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def valid_suffix(suffix):
    """
    验证合法的图片后缀
    """
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('请先登录', 'error')
            return redirect(url_for('index.login'))
        return f(*args, **kwargs)
    return decorated_function


def author_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        models = {
            'topic': Topic,
            'reply': Reply,
        }
        # 根据蓝图名选择对应的 model
        model = models.get(request.blueprint)
        m_id = int(request.values.get('id'))
        m = model.find_by(id=m_id)
        u = g.user
        if m.user_id == u.id or u.admin is True:
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        u = g.user
        if u.admin is True:
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.values.get('token', None)
        if token == session.get('token', -1):
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorated_function