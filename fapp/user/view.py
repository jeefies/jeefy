"""
User login Blueprint
prefix : /user
"""
from urllib.parse import unquote as urldecode
from urllib.parse import urlencode

from .bp import user

from ..imps import *
from config import config

from itsdangerous.url_safe import URLSafeTimedSerializer

# @user.route("/test/login")
# def test_login():
#     Login("jeefy", 60 * 10)
#     flash("Login OK")
#     return "Login, OK, <a href='/'>Back to main</a>"
# 
# @user.route('/test/reset')
# def test_reset():
#     rsp = make_response(redirect('/'))
#     rsp.delete_cookie("Math")
#     flash("Reset OK")
#     return rsp

@user.route("/register")
def register():
    fill = False
    if request.args.get('fill') == 'yes':
        fill = True
    return render_template("user/register.html", olds = request.args, fill = fill)

def getRegisterData():
    return dict(
            name = request.form.get('name'),
            email = request.form.get('email'),
            sex = request.form.get('sex'),
            )

@user.route("/register_submit", methods=["POST", "GET"])
def register_submit():
    name = request.values.get('name')
    
    oldData = getRegisterData()
    oldData['fill'] = 'yes'
    if User.indexByName(name):
        flash("用户名已存在，请更改以继续")
        oldData.pop('name')
        return redirect(url_for(".register") + "?" + urlencode(oldData))

    email = request.values.get('email')
    if User.indexByEmail(email):
        flash("邮箱已经注册，请更改以继续")
        oldData.pop('email')
        return redirect(url_for(".register") + "?" + urlencode(oldData))

    sex = request.values.get('sex')
    sex = True if sex == '1' else False
    pwd = request.values.get('password')
    role = Role.getRole(request.values.get('role'))
    # print(role)

    new = User(name = name, email = email, sex = sex, password = pwd, role = role)
    db.session.add(new)
    db.session.commit()
    flash("注册成功")

    # send email confirm message
    # ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt="confirm")
    # etoken = ts.dumps([name, email])
    return redirect(url_for('.register_ok'))

@user.route('/register/ok')
def register_ok():
    return "Remember to check you email box to confirm your account"

@user.route('/me')
@LoginRequired
def me():
    userInfo = g.current_user
    user = User.indexByName(userInfo.userName)
    return render_template("user/me.html", info = user.json())

@user.route("/loginpage")
def login():
    needFull = False
    if request.args.get("full", None):
        needFull = True

    if request.args.get("from"):
        session['from'] = request.args.get("from")

    return render_template("user/login.html", needFull = needFull)

@user.route("/login", methods=["POST"])
def login_submit():
    name_or_email = request.form.get("userName")
    if '@' in name_or_email:
        user = User.indexByEmail(name_or_email)
    else:
        user = User.indexByName(name_or_email)
    if not user:
        flash("用户或密码错误，请重新输入")
        return redirect("/?activeLogin=True")

    pwd = request.form.get("password")
    if pwd != user.password:
        flash("用户或密码错误，请重新输入")
        return redirect("/?activeLogin=True")

    Login(user.name)
    flash("成功登录")
    if session.get("from"):
        fromUrl = urldecode(session.get('from'))
        session['from'] = None
        return redirect(fromUrl)
    return redirect("/")

@user.route('/signout')
def signout():
    Logout()
    flash("您已退出登陆状态")
    return redirect("/")

@user.route('/manage')
def manager():
    return "Manager"
