import os

base = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", 'hard to guess key')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base, 'data1.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class PyAnywhere(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://jeefy:mysqlpwd@jeefy.mysql.pythonanywhere-services.com/default"

class Debug(Config):
    DEBUG = True

class Heroku(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql://jeefy.mysql.pythonanywhere-services.com")
    SSL_REDIRECT = True if os.getenv('DYNO') else False
    PROXYFIX_USE = True if os.getenv('PROXYFIX_USE') else False

    @classmethod
    def init_app(cls, app):
        print('database url', cls.SQLALCHEMY_DATABASE_URI)
        if cls.PROXYFIX_USE:
            print('proxyfix use')
            from werkzeug.middleware.proxy_fix import ProxyFix
            app.wsgi_app = ProxyFix(app.wsgi_app)

config = {'config': Config,
        'default': Config,
        'debug': Debug,
        'heroku': Heroku
        }
