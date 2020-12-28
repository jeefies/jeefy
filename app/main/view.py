import os
import time
import zlib
import base64

from ..imps import *
from ..paths import JDB
from ..models import User

User = User(JDB, 'user')

__all__ = ('index',)

def regist(app):
    def _reg(func):
        method = getattr(func, 'method', ['GET'])
        name = func.__name__
        rule = getattr(func, 'rule')
        app.add_url_rule(rule, name, func, methods = method)

    for k in __all__:
        _reg(globals()[k])

def index():
    return "<h1>Hello</h1>"

index.rule = '/'
