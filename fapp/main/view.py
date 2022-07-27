"""
views:
    / (index): Index page of the site
    /favicon.ico: The image of the site
    /urls (urls): almost no use
"""
from functools import lru_cache

from .bp import main
from ..imps import *


@main.route('/')
def index():
    cur = g.current_user
    name = cur.userName if cur else "stranger"
    print(request.cookies)
    activeLogin = True if request.args.get('activeLogin') == "True" else False
    return render_template('base.html', name = name, activeLogin = activeLogin)

@main.route("/favicon.ico")
def _pic():
    return redirect(url_for('static', filename='favicon.ico'))

@main.route('/urls')
@lru_cache()
def urls():
    ds = dict(data = url_for('js.data'),
            self = url_for('user.listus') + '?self=true')
    return jsonify(ds)
