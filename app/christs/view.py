from functools import lru_cache

from ..imps import *
from ..reg import regist as reg

__all__ = ('xsh', 'cg', 'xyx', 'wgcy', 'zly', 'teach')

def regist(app):
    reg(app, globals(), __all__)

@lru_cache()
def xsh():
    return render_template('chris/xsh.html')

xsh.rule = '/xsh'

@lru_cache()
def cg():
    return render_template('chris/cg.html')

cg.rule = '/cg'

@lru_cache()
def xyx():
    return render_template('chris/xyx.html')

xyx.rule = '/xyx'

@lru_cache()
def wgcy():
    return render_template('chris/wgcy.html')

wgcy.rule = '/wgcy'

@lru_cache()
def zly():
    return render_template('chris/zly.html')

zly.rule = '/zly'

@lru_cache()
def teach():
    return render_template('chris/teacher.html')

teach.rule = '/teach'
