import os

from flask import Flask
from config import SECRET_KEY
from routes.index import index_bp
from routes.admin import admin_bp
from routes.topic import topic_bp
from routes.reply import reply_bp
from routes.mail import mail_bp
from routes.user import user_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    # 设置 secret_key 以使用 flask 自带的 session
    app.secret_key = SECRET_KEY
    app.register_blueprint(index_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(topic_bp, url_prefix='/topic')
    app.register_blueprint(reply_bp, url_prefix='/reply')
    app.register_blueprint(mail_bp, url_prefix='/mail')
    # 注册 Jinja2 模板中使用的全局函数 现在用g.user代替了
    # app.jinja_env.globals['current_user'] = current_user
    return app

app = create_app()