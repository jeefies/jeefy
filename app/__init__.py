from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.login_view = 'user.login'

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

    from ._cfile import file as file_bp
    app.register_blueprint(file_bp, url_prefix="/f")

    from .file import mfile as mfile_bp
    app.register_blueprint(mfile_bp, url_prefix="/fi")

    from .user import user as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    from .js import js as js_bp
    app.register_blueprint(js_bp, url_prefix = "/js")

    return app
