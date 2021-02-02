"""
views:
    / (index): Index page of the site
    /favicon.ico: The image of the site
    /urls (urls): almost no use
"""
from functools import lru_cache

from ..imps import *
from ..reg import regist as reg

from flask_login import current_user


__all__ = ('index', "_pic", 'urls')

def regist(app):
    reg(app, globals(), __all__)

def index():
    @lru_cache()
    def r(cur):
        return render_template('base.html')
    return r(current_user)

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
