from urllib.parse import urlencode

from flask import Flask, flash, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
# from .reg import unauthorized_handler

from .login import LoginManager

db = SQLAlchemy()
loginManager = LoginManager()
mail = Mail()
# login manager config
# loginmanager = LoginManager()
# loginmanager.login_view = 'user.login'
# loginmanager.login_message = "Please log in first!"
# loginmanager.unauthorized_callback = unauthorized_handler

def unauthorized_processor():
    flash("您还未登陆，请登陆后再查看")
    args = {'full' : 'true', 'from' : request.path}
    return redirect(url_for("user.login") + '?' + urlencode(args))

loginManager.set_not_login_processor(unauthorized_processor)


def create_app(cfg):
    print(cfg)
    app = Flask(__name__)
    conf = config[cfg]
    app.config.from_object(conf)
    conf.init_app(app)
    print(conf.SQLALCHEMY_DATABASE_URI)

    if app.config.get('SSL_REDIRECT', False):
        from flask_sslify import SSLify
        sslify = SSLify(app)

    loginManager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    # loginmanager.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .user import user as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")
    
    from .room import room as room_bp
    app.register_blueprint(room_bp, url_prefix="/chat")

    from .file import file as file_bp
    app.register_blueprint(file_bp, url_prefix="/files")

    from .song163 import song as song_bp
    app.register_blueprint(song_bp, url_prefix="/song163")

    from .luoguGame import luoguGame as luoguGame_bp
    app.register_blueprint(luoguGame_bp, url_prefix="/luoguGame")
    return app
