import io
import os
from base64 import b16encode as b16en
from base64 import b16decode as b16de

from .fm import Files, toZipIO
from .forms import FileForm
from ..paths import FILEPATH
from ..imps import *
from ..reg import regist as reg

__all__ = ('index', 'download', 'readf')

def regist(app):
    reg(app, globals(), __all__)


def index():
    form = FileForm()
    if form.validate_on_submit():
        data = form.file.data
        Files.wtfwrite(data)
        flash('Upload Succeed!')
        form.iupdate()
    resp = mkrsp(render_template('file/index.html', form = form))
    resp.set_cookie('name', 'jeefy')
    return resp

index.rule = '/'
index.method = ['GET', 'POST']

def tb(s):
    if isinstance(s, str):
        return s.encode()
    elif isinstance(s, (bytes, bytearray)):
        return s
    else:
        return str(s).encode()

def ts(b):
    if isinstance(b, str):
        return b
    elif isinstance(b, (bytes, bytearray)):
        return b.decode()
    return str(b)

def enfn(fn):
    return ts(b16en(tb(fn)))

def defn(fn):
    return ts(b16de(tb(fn)))

def download():
    f = [(url_for('.readf', fn=enfn(f)), f) for f in Files.listname()]
    print(f)
    return render_template('file/files.html', files=f)

download.rule = "/files"

def readf(fn):
    fn = defn(fn)
    rfn, fio = Files.read(fn)
    rsp = mkrsp(send_file(fio, attachment_filename = rfn, as_attachment=True))
    return rsp

readf.rule = "/dl/<fn>"
