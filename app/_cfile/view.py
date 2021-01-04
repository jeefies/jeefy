import io
import os
import gzip
import time
from base64 import b16encode as b16en
from base64 import b16decode as b16de

from jetz import ZipFile
from json import dumps
from flask import jsonify

from .forms import FileForm
from ..gls import FILEPATH
from ..imps import *
from ..reg import regist as reg

__all__ = ('index', 'download', 'readf', 'delf')

Files = ZipFile()
_t = time.time()
S = 1
try:
    Files.read(os.path.join(FILEPATH, 'files.zip'))
except FileNotFoundError:
    pass
except Exception as e:
    S = 0

def check():
    global _t, S
    if time.time() - _t > 5:
        if S:
            try:
                Files.save(os.path.join(FILEPATH, 'files.zip'))
                print('saving success')
            except Exception as e:
                S = 0
                print(e)
        _t = time.time()

def regist(app):
    reg(app, globals(), __all__)


def index():
    form = FileForm()
    if form.validate_on_submit():
        data = form.file.data
        Files.add_form_data(data)
        flash('Upload Succeed!')
        check()
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
    f = [(url_for('.readf', fn=enfn(f)), f) for f in Files.list()]
    return render_template('file/files.html', files=f)

download.rule = "/files"

def readf(fn):
    fn = defn(fn)
    fio = io.BytesIO(gzip.compress(Files.get(fn)))
    rfn = fn + '.gz'
    rsp = mkrsp(send_file(fio, attachment_filename = rfn, as_attachment=True))
    rsp.headers['Content-Type'] = "application/gzip"
    return rsp

readf.rule = "/dl/<fn>"

def delf(fn):
    fn = defn(fn)
    f, c = Files.remove(fn)
    di = dict(filename = f, content = dumps(tuple(c)))
    rsp = mkrsp(dumps(di, indent = 4))
    rsp.headers['Content-Type'] = 'application/json'
    check()
    return rsp

delf.rule = "/del/<fn>"
