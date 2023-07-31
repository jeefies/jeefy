"""
views:
    / (index): Index page of the site
    /favicon.ico: The image of the site
"""
from functools import lru_cache

from .bp import main
from ..imps import *


@main.route('/')
def index():
    cur = g.current_user
    name = cur.userName if cur else "stranger"
    # print(request.cookies)
    activeLogin = True if request.args.get('activeLogin') == "True" else False
    return render_template('base.html', name = name, activeLogin = activeLogin)

@main.route("/favicon.ico")
def _pic():
    return redirect(url_for('static', filename='favicon.ico'))

@main.route('/secKey')
def secKey():
    return current_app.config['SECRET_KEY']
