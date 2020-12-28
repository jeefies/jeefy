import os

base = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", 'hard to guess key')

    @staticmethod
    def init_app(app):
        pass


class Debug(Config):
    DEBUG = True

config = {'config': Config,
        'default': Config,
        'debug': Debug
        }
