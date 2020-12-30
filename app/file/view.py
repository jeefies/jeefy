import os

from ..paths import FILEPATH
from ..imps import *
from .forms import FileForm
from ..reg import regist as reg

__all__ = ('index', 'download', 'downloadm')

def regist(app):
    reg(app, globals(), __all__)


def index():
    form = FileForm()
    if form.validate_on_submit():
        data = form.file.data
        name = data.filename
        p = os.path.join(FILEPATH, name)
        flash('Upload Succeed!')
        data.save(p)
        form.iupdate()
    return render_template('file/index.html', form = form)

index.rule = '/'
index.method = ['GET', 'POST']

def download(stcp):
    viewp = os.path.join(FILEPATH, stcp)
    return check(viewp, stcp)

download.rule = '/path/<path:stcp>'

def downloadm():
    return check(FILEPATH, '')

downloadm.rule = '/path'

def check(stcp, start):
    dirs = os.listdir(stcp)
    d = []
    adp = d.append
    f = []
    afp = f.append
    isf = os.path.isfile
    absp = os.path.abspath
    join = os.path.join
    for i in dirs:
        a = absp(join(FILEPATH, start, i))
        print(a)
        p = join(start, i) if start else i
        if isf(a):
            afp((url_for('static', filename=p), i))
        else:
            adp((url_for('.download', stcp = p), i))
    return render_template('file/files.html', files=f, dirs=d)
