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
from models.mail import Mail
from models.user import User
from . import (
    login_required,
    token_required,
)

mail_bp = Blueprint('mail', __name__)


@mail_bp.route('/')
@login_required
def index():
    u_id = g.user.id
    unread_mails = Mail.find_all(receiver_id=u_id, read=False, __sort=('created_time', -1))
    old_mails = Mail.find_all(receiver_id=u_id, read=True, __sort=('created_time', -1))
    sent_mails = Mail.find_all(sender_id=u_id, url=False, __sort=('created_time', -1))
    return render_template('mail/index.html', unread_mails=unread_mails, old_mails=old_mails, sent_mails=sent_mails)


@mail_bp.route('add', methods=['Post'])
@login_required
@token_required
def send():
    form = request.form
    u = g.user
    if Mail.send_mail(form, sender_id=u.id) is True:
        flash('发送消息成功', 'success')
    else:
        flash('发送消息失败，用户不存在或未填写标题', 'error')
    return redirect(url_for('mail.index'))


@mail_bp.route('read_all')
@login_required
@token_required
def read_all():
    unread_mails = Mail.find_all(receiver_id=g.user.id, read=False)
    for m in unread_mails:
        m.mark_read()
    return redirect(url_for('mail.index'))


@mail_bp.route('/<int:m_id>')
@login_required
def detail(m_id):
    m = Mail.find_by(id=m_id)
    if m is None:
        abort(404)
    elif g.user.id not in (m.sender_id, m.receiver_id):
        abort(403)
    else:
        m.mark_read()
        if m.url:
            return redirect(m.content)
        else:
            return render_template('mail/detail.html', m=m)


def users_from_content(content):
    intab = '.,?!。，、？！'
    outtab = ' '
    table = str.maketrans(intab, outtab*len(intab))
    parts = content.translate(table).split()
    users = []
    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.find_by(username=username)
            if u is not None:
                users.append(u)
    return users


def inform_users(content, url):
    sender = g.user
    receivers = users_from_content(content)
    for r in receivers:
        form = dict(
            title='用户 “{}” AT 了你'.format(sender.username),
            content=url,
            sender_id=sender.id,
            receiver_id=r.id,
            url=True,
        )
        Mail.new(form)
