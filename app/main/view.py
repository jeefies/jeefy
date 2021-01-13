import os
import time
import zlib
import base64
from functools import lru_cache

from ..imps import *
from ..reg import regist as reg

__all__ = ('index', "_pic", 'urls')

def regist(app):
    reg(app, globals(), __all__)

@lru_cache()
def index():
    return render_template('base.html')

index.rule = '/'

def _pic():
    return redirect(url_for('static', filename='favicon.ico'))

_pic.rule = '/favicon.ico'

@lru_cache()
def urls():
    ds = dict(data = url_for('js.data'),
            self = url_for('user.listus') + '?self=true')
    return jsonify(ds)

urls.rule = '/urls'
