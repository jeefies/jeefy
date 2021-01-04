import io
import os
import gzip
import time
from base64 import b16encode as b16en
from base64 import b16decode as b16de

from json import dumps as jdumps

from .forms import FileForm
from .. import db
from ..gls import FILEPATH
from ..imps import *
from ..reg import regist as reg
from ..models import File, User

__all__ = ('index', 'download', 'readf', 'delf')

def regist(app):
    reg(app, globals(), __all__)


def bf_req():
    un = session.get('name', None)
    if not un:
        abort(401)


def index():
    form = FileForm()
    if form.validate_on_submit():
        data = form.file.data
        file = File.add_form_data(data)
        db.session.add(file)
        db.session.commit()
        flash('Upload Succeed!')
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
    f = [(url_for('.readf', fn=enfn(f)), f) for f in File.list()]
    return render_template('file/files.html', files=f)

download.rule = "/files"

def readf(fn):
    fn = defn(fn)
    file = File.query.filter_by(fn = fn).first_or_404()
    rfn, fi = file.info()
    fio = io.BytesIO(fi)
    rsp = mkrsp(send_file(fio, attachment_filename = rfn, as_attachment=True))
    rsp.headers['Content-Type'] = "application/gzip"
    return rsp

readf.rule = "/dl/<fn>"

def delf(fn):
    fn = defn(fn)
    file = File.query.filter_by(fn = fn).first_or_404()
    db.session.delete(file)
    db.session.commit()
    fn, ct = file.info()
    di = dict(filename = fn, warn = ("content is a bytes array. "
        "After turning into python list, "
        "use bytes(thelist) to convert it back to bytes"),
        content = jdumps(tuple(ct)))
    rsp = mkrsp(jdumps(di, indent = 4))
    rsp.headers['Content-Type'] = "application/json"
    return rsp

delf.rule = '/del/<fn>'
