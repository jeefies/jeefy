import io
import os
import gzip
import time
from base64 import b16encode as b16en
from base64 import b16decode as b16de
from functools import lru_cache

from json import dumps as jdumps

from .forms import FileForm
from .. import db
from ..imps import *
from ..reg import regist as reg
from ..models import File, User

from flask_login import current_user

__all__ = ('index', 'download', 'readf', 'delf', 'showf', 'changecon', 'chname')

def printr(x):
    print(x)
    return x

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
        file.user = current_user
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
    l = File.list(current_user)
    try:
        f = [(url_for('.showf', fn=enfn(f)), f, u) for f, u in File.list(current_user)]
    except:
        return l
    return render_template('file/files.html', files=f)

download.rule = "/files"

def urls(fn):
    return dict(dl = url_for('.readf', fn = fn),
            upl = url_for('.changecon', fn = fn),
            ren = url_for('.chname', fn = fn),
            show = url_for('.showf', fn = fn),
            dele = url_for('.delf', fn = fn))

def showf(fn):
    f = defn(fn)
    file = File.query.filter_by(fn = f).first_or_404()

    return render_template('file/show.html', f = file, urls = urls(fn))

showf.rule = "/show/<fn>"

@lru_cache()
def readf(fn):
    fn = defn(fn)
    file = File.query.filter_by(fn = fn).first_or_404()
    rfn, fi = file.info()
    fio = io.BytesIO(fi)
    rsp = mkrsp(send_file(fio, attachment_filename = rfn, as_attachment=True))
    rsp.headers['Content-Type'] = "application/octet-stream"
    rsp.headers['Content-Encoding'] = "gzip"
    rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % rfn.encode()).decode('latin-1')
    return rsp

readf.rule = "/dl/<fn>"


def changecon(fn):
    ctx = req.values.get('ctx')
    n = defn(fn)
    file = File.query.filter_by(fn = n).first_or_404()
    file.ctx = ctx.encode()
    db.session.add(file)
    db.session.commit()
    return jsonify({'code': 200, 'success': True})

changecon.rule = '/cc/<fn>'
changecon.method = {'POST', 'GET'}

def chname(fn):
    newn = req.values.get('name')
    n = defn(fn)
    if newn == n:
        return jsonify({'code': 200, 'success': True, 'reload': False})
    file = File.query.filter_by(fn = n).first_or_404()
    file.fn = newn
    file.ctx = file.ctx
    db.session.add(file)
    db.session.commit()
    return jsonify({'code': 200, 'success': True, 'reload': True, 'url': url_for('.showf', fn = enfn(newn))})

chname.rule = '/cn/<fn>'
chname.method = {'POST', 'GET'}

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
