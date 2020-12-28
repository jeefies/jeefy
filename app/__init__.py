from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()

def create_app(cfg):
    app = Flask(__name__)
    conf = config[cfg]
    app.config.from_object(conf)
    conf.init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .christs import chri as chri_bp
    app.register_blueprint(chri_bp, url_prefix="/chris")

    return app
