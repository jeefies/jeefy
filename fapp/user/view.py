"""
User login Blueprint
prefix : /user
"""
from urllib.parse import unquote as urldecode

from .bp import user

from ..imps import *
from config import config

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
    return render_template("user/register.html")

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
    flash("您以退出登陆状态")
    return redirect("/")

@user.route('/manage')
def manager():
    return "Manager"
