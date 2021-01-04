#from json import dumps

from flask_login import login_user, login_required, logout_user, current_user

from ..models import User, Role
from ..imps import *
from .. import db
from .bp import user
from .forms import RegistForm, LoginForm


@user.route('/new', methods = ["GET", "POST"])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        admin = Role.query.filter_by(name = 'admin').first()
        name = form.name.data
        email = form.name.data
        pwd = form.pwd.data
        if User.query.filter_by(name = name).all():
            flash('The name has been registed!')
            return redirect(url_for('.index'))
        elif User.query.filter_by(email = email).all():
            flash("The email is already in used")
            return redirect(url_for('.index'))
        user = User(name = name, email = email, role = admin, age = 1, password = pwd)
        db.session.add(user)
        db.session.commit()
        flash("regist success")
        return redirect(url_for('.index'))
    return render_template('user/regist.html', form = form)

@user.route('/login/<name>/<password>')
def login(name, password):
    rem = req.args.get('remember')
    rem = True if rem else False
    user = User.query.filter_by(name = name, password = password).first()
    if not user:
        flash("User Info Doesn't match!")
        return redirect(url_for('.loginpage'))
    login_user(user, rem)
    flash("Login success!")
    return redirect(url_for('main.index'))

@user.route('/login', methods = ['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        url = url_for('.login', name = form.name.data, password = form.pwd.data)
        if form.rem:
            url += "?remember=1"
        return redirect(url)
    return render_template("user/login.html", form = form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))

@user.route('/u/<name>')
def see(name):
    user = User.query.filter_by(name = name).first_or_404()
    return render_template('user/user.html', user = user)

@user.route('/')
def index():
    return render_template('user/index.html')

@user.route('/list')
def listus():
    if req.args.get('self') == 'true':
        try:
            user = User.query.filter_by(name = current_user.name).first()
            if user:
                return jsonify(user.json())
        except:
            pass
    return render_template('user/users.html', users = User.query.all())

@user.route('/self')
@login_required
def self():
    return redirect(url_for('.user', name = current_user.name))

