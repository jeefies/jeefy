from ..imps import *
from ..reg import regist as reg

__all__ = ('xsh', 'cg', 'xyx', 'wgcy', 'zly', 'teach')

def regist(app):
    reg(app, globals(), __all__)

def xsh():
    return render_template('chris/xsh.html')

xsh.rule = '/xsh'

def cg():
    return render_template('chris/cg.html')

cg.rule = '/cg'

def xyx():
    return render_template('chris/xyx.html')

xyx.rule = '/xyx'

def wgcy():
    return render_template('chris/wgcy.html')

wgcy.rule = '/wgcy'

def zly():
    return render_template('chris/zly.html')

zly.rule = '/zly'

def teach():
    return render_template('chris/teacher.html')

teach.rule = '/teach'
