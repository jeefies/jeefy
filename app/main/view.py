import os
import time
import zlib
import base64

from ..imps import *
from ..paths import JDB
from ..reg import regist as reg

__all__ = ('index', "_pic")

def regist(app):
    reg(app, globals(), __all__)

def index():

    print(url_for('static', filename='favicon.ico'))
    return "<h1>Hello</h1>"

index.rule = '/'

def _pic():
    return redirect(url_for('static', filename='favicon.ico'))

_pic.rule = '/favicon.ico'
