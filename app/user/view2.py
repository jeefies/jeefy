"""
views:
    / (index)
    /u/<name> : user's info(filte by the name)
    /self: redirect to self info page
    /user-detail (more): More info
    /--list (listus): List All the users has registed
"""
from .bp import user
from ..models import User, db
from ..imps import *
from .forms import DetailForm

from flask_login import login_user, login_required, logout_user, current_user


@user.route('/')
def index():
    return render_template('user/index.html')

@user.route('/u/<name>')
def see(name):
    user = User.query.filter_by(name = name).first_or_404()
    self = user == current_user
    print(self)
    return render_template('user/user.html', user = user, self = self)

@user.route('/self')
@login_required
def self():
    return redirect(url_for('.see', name = current_user.name))

@user.route('/--list')
def listus():
    if req.args.get('self') == 'true':
        try:
            user = User.query.filter_by(name = current_user.name).first()
            if user:
                return jsonify(user.json())
        except:
            pass
    return render_template('user/all.html', users = User.query.all())

@user.route('/user-detail', methods = ["GET", "POST"])
@login_required
def more():
    user = current_user
    form = DetailForm()
    if form.validate_on_submit():
        user.birth = form.birth.data
        s = form.sex.data
        user.sex = 0 if s == "Male" else 1
        user.desc = form.desc.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(".self"))
    form.birth.data = user.birth
    form.sex.data = user.sex
    form.desc.data = user.desc
    return render_template("user/detail.html", form = form)
