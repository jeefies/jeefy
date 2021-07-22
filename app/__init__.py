from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from .reg import unauthorized_handler

moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
# login manager config
loginmanager = LoginManager()
loginmanager.login_view = 'user.login'
loginmanager.login_message = "Please log in first!"
loginmanager.unauthorized_callback = unauthorized_handler


def create_app(cfg):
    print(cfg)
    app = Flask(__name__)
    conf = config[cfg]
    app.config.from_object(conf)
    conf.init_app(app)
    print(conf.SQLALCHEMY_DATABASE_URI)

    if app.config.get('SSL_REDIRECT', False):
        print('redirect')
        from flask_sslify import SSLify
        sslify = SSLify(app)

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    loginmanager.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .christs import chri as chri_bp
    app.register_blueprint(chri_bp, url_prefix="/chris")

    from .file import mfile as mfile_bp
    app.register_blueprint(mfile_bp, url_prefix="/fi")

    from .user import user as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    from .js import js as js_bp
    app.register_blueprint(js_bp, url_prefix="/js")

    from .birth import birth as birth_bp
    app.register_blueprint(birth_bp, url_prefix="/birth")

    from .g163song import song as song_bp
    app.register_blueprint(song_bp, url_prefix="/163song")

    from .n2021_1_video import video as video_bp
    app.register_blueprint(video_bp, url_prefix="/video/school")

    from .room import room as room_bp
    app.register_blueprint(room_bp, url_prefix="/chatroom")

    from .help import jhelp as help_bp
    app.register_blueprint(help_bp, url_prefix="/help")

    return app
