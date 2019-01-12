from flask import (
    render_template,
    request,
    redirect,
    Blueprint,
    flash,
    g,
    abort,
    url_for,
)
from models.topic import Topic
from models.reply import Reply
from routes.mail import inform_users
from . import (
    login_required,
    author_or_admin_required,
    token_required,
)

reply_bp = Blueprint('reply', __name__)


@reply_bp.route('/add', methods=["POST"])
@login_required
@token_required
def add():
    form = request.form
    r = Reply.new(form, user_id=g.user.id)
    Topic.replied(r)
    url = url_for('topic.detail', t_id=r.topic_id, _anchor=r.topic().num_of_replies())
    inform_users(form.get('content'), url)
    return redirect(request.referrer)


@reply_bp.route("/edit/<int:r_id>")
@login_required
def edit(r_id):
    r = Reply.find_by(id=r_id)
    if r is None:
        abort(404)
    else:
        return render_template('reply/edit.html', reply=r)


@reply_bp.route("/update", methods=["POST"])
@login_required
@author_or_admin_required
@token_required
def update():
    form = request.form
    r_id = int(form.get('id'))
    r = Reply.find_by(id=r_id)
    r.update_reply(form)
    flash('修改回复成功', 'success')
    return redirect(form.get('next'))


@reply_bp.route("/delete")
@login_required
@author_or_admin_required
@token_required
def delete():
    r_id = int(request.args.get('id'))
    r = Reply.find_by(id=r_id)
    r.delete()
    flash('删除回复成功', 'success')
    return redirect(request.referrer)
