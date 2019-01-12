from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
    abort,
    g,
)
from models.board import Board
from models.topic import Topic
from routes.mail import inform_users
from . import (
    login_required,
    author_or_admin_required,
    token_required,
)

topic_bp = Blueprint('topic', __name__)


@topic_bp.route('/create')
@login_required
def create():
    bs = Board.find_all()
    return render_template('topic/create.html', bs=bs)


@topic_bp.route("/add", methods=["POST"])
@login_required
@token_required
def add():
    form = request.form
    u = g.user
    t = Topic.new(form, user_id=u.id)
    url = url_for('topic.detail', t_id=t.id)
    inform_users(form.get('content'), url)
    return redirect(url)


@topic_bp.route('/<int:t_id>')
def detail(t_id):
    # get调用了find_by方法，同时浏览数+1
    t = Topic.get(t_id)
    if t is None:
        abort(404)
    else:
        u = t.user()
        # 传递 topic 的所有 reply 到 页面中
        return render_template("topic/detail.html", topic=t, author=u)


@topic_bp.route("/delete")
@login_required
@author_or_admin_required
@token_required
def delete():
    t_id = int(request.args.get('id'))
    t = Topic.find_by(id=t_id)
    t.delete()
    flash('删除话题成功', 'success')
    return redirect(url_for('index.index'))


@topic_bp.route("/edit/<int:t_id>")
@login_required
def edit(t_id):
    t = Topic.find_by(id=t_id)
    if t is None:
        abort(404)
    else:
        bs = Board.find_all()
        return render_template("topic/edit.html", topic=t, bs=bs)


@topic_bp.route("/update", methods=["POST"])
@login_required
@author_or_admin_required
@token_required
def update():
    form = request.form
    t_id = int(form.get('id'))
    t = Topic.find_by(id=t_id)
    t.update_topic(form)
    flash('修改话题成功', 'success')
    return redirect(form.get('next'))

