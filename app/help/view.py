from .bp import jhelp as app
from ..imps import *

@app.route('/')
def index():
    return '<h1>Help</h1>'

@app.route('/profile-image')
def profile_image():
    con = "First, We use <a href='www.gravatar.com'>gravatar.com</a> to generate your profile image.\n";
    con += "Don't be worry, use your email to sing up and upload your profile there.\n";
    con += "It's free of course and many sites are also use it like <a href='https://pypi.org'>PyPI</a>\n";
    con += "After you upload your image there, if it's not shown there, please check if your email if right\n";
    con += "Go <a href='/user/self'>Here</a> to check your email.\n";
    con += "Hope you can enjoy yourself!\n";
    con += "<samll>Thanks for your support</small>";
    return con.replace('\n', '<br>')
