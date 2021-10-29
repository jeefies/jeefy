"""
Views:
    /new(regist): regist a new user
    /login(loginpage): a html page to login. redirect the data to /login/<name>/<password>
    /login/<name>/<password>(login): a api to login(name can be email)
    /logout(logout): logout the account has logged in
"""
from flask_login import login_user, login_required, logout_user, current_user

from ..models import User, Role
from ..imps import *
from .. import db
from .bp import user
from .forms import RegistForm, LoginForm


@user.route('/new', methods = ["GET", "POST"])
def regist():
    Role.checkRole()
    form = RegistForm()
    if form.validate_on_submit():
        # get the general infomations
        name = form.name.data
        email = form.email.data # fix issue: could not login with email (参数写错了)
        pwd = form.pwd.data
        role = form.role.data
        
        # get the role given by the register
        role = Role.query.filter_by(name = role).first()
        
        # check if it's already exitsts
        if User.query.filter_by(name = name).all():
            flash('The name has been registed!')
            return redirect(url_for('.index'))
        elif User.query.filter_by(email = email).all():
            flash("The email is already in used")
            return redirect(url_for('.index'))
        # validate info !
        # continue to add it into database
        user = User(name = name, email = email, role = role, password = pwd)
        db.session.add(user)
        db.session.commit()
        flash("regist success")
        return redirect(url_for('.loginpage'))
    return render_template('user/regist.html', form = form)

@user.route('/login/<name>/<password>')
def login(name, password):
    # check if need to set cookies to remeber login
    rem = req.args.get('remember')
    rem = True if rem else False
    
    user = User.query.filter_by(name = name, password = password).first()
    if not user:
        user = User.query.filter_by(email = name, password = password).first()
    if not user:
        flash("User Info Doesn't match!")
        return redirect(url_for('.loginpage'))
    login_user(user, rem)
    flash("Login success!")
    
    # check if need to redirect to origin page
    back = req.args.get("back", '')
    if back:
        return redirect(back)
    
    return redirect(url_for('main.index'))

@user.route('/login', methods = ['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        # get the url for login to redirect to
        # remember password is not crypted!
        url = url_for('.login', name = form.name.data, password = form.pwd.data)
        
        # check if need  to set cookie to remeber login
        if form.rem:
            url += "?remember=1"
            
        # check if need to redirect to origin page
        back = req.args.get("back", '')
        if back:
            url += "&back=" + back
        return redirect(url)
    
    return render_template("user/login.html", form = form)

@user.route('/logout')
@login_required
def logout():
    logout_user() # define in flask_login
    # show the message of logout operation
    flash("You have been logged out")
    return redirect(url_for('main.index'))
