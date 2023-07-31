import os

base = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(16).hex())
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base, 'data1.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGIN_EXPIRE_TIME = 60 * 60 * 24 * 3 # 3 days

    @staticmethod
    def init_app(app):
        print(app.config['SECRET_KEY'])
        pass

class Debug(Config):
    DEBUG = True


config = {'config': Config,
        'default': Config,
        'debug': Debug,
        }
