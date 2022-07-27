from functools import wraps
import time
import math

from config import config
from flask import make_response, request, g, abort, redirect
from itsdangerous.url_safe import URLSafeSerializer as Serializer

loginStateCookieName = "Math"
notLoginProcessor = None

auth_s = Serializer(config["default"].SECRET_KEY, salt="login")

class LoginManager:
    def __init__(self, app = None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(preLoginHandler)
        app.after_request(afterLoginHandler)
        app.add_template_global(get_current_user, "current_user")
        app.add_template_global(lambda: True if g.current_user else False, "user_logined")

class UserInfo:
    userName = None
    expireTime = 0
    lastCheck = 0
    infoDict = None

    def __init__(self, loginCookie = None):
        if loginCookie:
            infoDict = auth_s.loads(loginCookie)
            # print("info dict", infoDict)
            self.userName = infoDict['un']
            self.expireTime = infoDict['et']
            self.lastCheck = infoDict['lc']

    def validLogin(self) -> bool:
        # print(self.expireTime, self.lastCheck, time.time())
        if self.expireTime + self.lastCheck < time.time():
            return False
        return True

    def toCookie(self) -> str:
        infoDict = dict()
        infoDict['un'] = self.userName
        infoDict['et'] = self.expireTime
        infoDict['lc'] = self.lastCheck
        print(infoDict)
        return auth_s.dumps(infoDict)

def LoginRequired(func):
    @wraps(func)
    def LoginRequiredWrapper(*args, **kwargs):
        if not g.current_user:
            abort(401)
    
        if g.current_user.validLogin():
            return func(*args, **kwargs)
        else:
            Logout()
            return redirect(request.url)
    return LoginRequiredWrapper

# expireTime should be an int of seconds
def Login(name, expireTime: int = -1):
    userInfo = UserInfo()
    userInfo.userName = name
    userInfo.lastCheck = math.ceil(time.time())
    if expireTime == -1 or not isinstance(expireTime, int):
        expireTime = config['default'].LOGIN_EXPIRE_TIME
    userInfo.expireTime = expireTime

    g.current_user = userInfo
    g.set_login_cookie = True

def Logout():
    if g.current_user:
        g.current_user.expireTime = 0


def get_current_user():
    return g.current_user

def preLoginHandler():
    loginCookie = request.cookies.get(loginStateCookieName)
    # print("pre-login handler call, cookie get", loginCookie)

    g.set_login_cookie = False
    if not loginCookie:
        g.current_user = None
    else:
        try:
            g.current_user = UserInfo(loginCookie)
        except Exception as e:
            # print("Get user info falied", e)
            g.current_user = None
            g.invalid_cookie = True

def afterLoginHandler(response):
    cur = g.current_user
    if not cur:
        return response

    if g.set_login_cookie == True and cur != None:
        # print("set cookie to", cur.toCookie())
        response.set_cookie(loginStateCookieName, cur.toCookie())
    elif not cur.validLogin() or g.get('invalid_cookie', False):
        print("del cookie, invalid_cookie is", g.get('invalid_cookie', False))
        response.set_cookie(loginStateCookieName, '')
    return response