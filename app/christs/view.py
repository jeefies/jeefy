from ..imps import *
from ..reg import regist as reg

__all__ = ('xsh', 'teach')

def regist(app):
    reg(app, globals(), __all__)

def xsh():
    return render_template('xsh.html')

xsh.rule = '/xsh'

def teach():
    return render_template('teacher.html')

teach.rule = '/teach'
