from flask import flash, redirect, url_for, request


def regist(app, gls, all_):
    def _reg(func):
        method = getattr(func, 'method', ['GET'])
        name = func.__name__
        rule = getattr(func, 'rule')
        app.add_url_rule(rule, name, func, methods=method)

    for k in all_:
        _reg(gls[k])


def unauthorized_handler():
    flash("Please Log in First!")
    return redirect(url_for('user.loginpage') + '?back=' + request.path)
