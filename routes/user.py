from flask import (
    render_template,
    request,
    redirect,
    session,
    g,
    url_for,
    Blueprint,
    flash,
    abort,
)
from models.user import User
from models.topic import Topic
from models.reply import Reply
import os
import uuid
from . import (
    login_required,
    token_required,
    valid_suffix,
)

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile/<username>')
def profile(username):
    u = User.find_by(username=username)
    if u is None:
        abort(404)
    else:
        ts = Topic.find_all(user_id=u.id, __sort=['created_time', -1], __slice=[0, 5])
        rt_ids = Reply.find_distinct(key='topic_id', page=1, page_size=5, user_id=u.id)
        rts = [Topic.find_by(id=rt_id) for rt_id in rt_ids]
        return render_template('user/profile.html', user=u, ts=ts, rts=rts)


@user_bp.route('/topics')
def topics():
    u_id = int(request.args.get('id'))
    u = User.find_by(id=u_id)
    if u is None:
        abort(404)
    else:
        page = int(request.args.get('page', 1))
        ts = Topic.find_page(page=page, user_id=u.id, __sort=['created_time', -1])
        pages = Topic.pages(user_id=u.id)
        return render_template('user/topics.html', user=u, ts=ts, page=page, pages=pages)


@user_bp.route('/replies')
def replies():
    u_id = int(request.args.get('id'))
    u = User.find_by(id=u_id)
    if u is None:
        abort(404)
    else:
        page = int(request.args.get('page', 1))
        t_ids = Reply.find_distinct(key='topic_id', page=page, user_id=u.id)
        ts = [Topic.find_by(id=t_id) for t_id in t_ids]
        pages = Reply.pages(__distinct='topic_id', user_id=u.id)
        return render_template('user/replies.html', user=u, ts=ts, page=page, pages=pages)


@user_bp.route('/login', methods=['Post'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 登录失败转回原页面
        flash('登录失败，用户名或密码错误', 'error')
        return redirect(url_for('index.login'))
    else:
        flash('登录成功，欢迎', 'success')
        # session 中写入 user_id 和 token
        session['user_id'] = u.id
        session['token'] = str(uuid.uuid4())
        # 设置 cookie 有效期为 持久，默认过期时间1个月，可通过app.permanent_session_lifetime修改
        session.permanent = True
        # 重定向到登陆前所在页面
        url = form.get('next', url_for('index.index'))
        return redirect(url)


@user_bp.route('/register', methods=['Post'])
def register():
    form = request.form
    u = User.register(form)
    if u is not None:
        flash('注册成功，请登录', 'success')
        return redirect(url_for('index.login'))
    else:
        flash('注册失败，用户名可能已被占用，或用户名和密码不合法', 'error')
        return redirect(url_for('index.register'))


@user_bp.route('/logout')
def log_out():
    # session.pop('user_id', None)
    session.clear()
    flash('登出成功，再见', 'success')
    return redirect(request.referrer)


@user_bp.route('/setting')
@login_required
def setting():
    return render_template('user/setting.html')


@user_bp.route('/data/update', methods=['Post'])
@login_required
@token_required
def update_data():
    u = g.user
    form = request.form
    u.update_data(form)
    flash('用户信息修改成功', 'success')
    return redirect(url_for('user.setting'))


@user_bp.route('/password/update', methods=['Post'])
@login_required
@token_required
def update_password():
    u = g.user
    form = request.form
    if u.update_password(form):
        flash('密码修改成功', 'success')
    else:
        flash('密码修改失败，当前密码错误，或新密码不合法', 'error')
    return redirect(url_for('user.setting'))


@user_bp.route('/avatar/update', methods=["POST"])
@login_required
@token_required
def update_avatar():
    u = g.user
    # file 是一个文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件要用 secure_filename 函数过滤文件名（防止文件上传漏洞），再加上时间戳（防止撞名）
        # filename = secure_filename(file.filename)
        # import time
        # filename = str(time.time()) + filename
        # 或直接用随机字符串重命名文件
        filename = '{0}.{1}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('static/uploads', filename))
        u.update_avatar(filename)
        flash('头像上传成功', 'success')
    else:
        flash('文件不合法', 'error')
    return redirect(url_for("user.setting"))


