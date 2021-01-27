"""
views:
    / (index):
        method=GET+POST, Index page, recv file and show the submit page
    /files (files):
        method=GET, return All the file owned, or public
    /dl/<fn> (readf):
        method=GET, return the file content
        (content-type: octet-stream, content-disposition: attachment;filename=...)
    /show/<fn> (showf):
        method=GET, the modify page of the file(or unsupport)
"""
import io
from base64 import b16encode as b16en
from base64 import b16decode as b16de

from json import dumps as jdumps

from .forms import FileForm
from .fdict import Fdict
from .bp import mfile
from .. import db
from ..imps import *
from ..models import File

from flask import current_app
from flask_login import current_user


fdict = Fdict()
app = mfile


@app.errorhandler(404)
def handler404(e):
    return render_template("file/404.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        data = form.file.data
        file = File.add_form_data(data, form.puc.data)
        if not file:
            flash("File already Exists!")
            return redirect(url_for(".index"))
        file.user = current_user
        fdict[file.fn] = file
        flash('Upload Succeed!')
        return redirect(url_for(".index"))
    resp = mkrsp(render_template('file/index.html', form=form))
    resp.set_cookie('name', 'jeefy')
    return resp


def enfn(s):
    if isinstance(s, str):
        return b16en(s.encode()).decode()
    elif isinstance(s, (bytes, bytearray)):
        return b16en(s).decode()
    else:
        return b16en(str(s).encode()).decode()


def defn(b):
    if isinstance(b, str):
        return b16de(b.encode()).decode()
    elif isinstance(b, (bytes, bytearray)):
        return b16de(b).decode()
    return b16de(str(b)).decode()


@app.route('/files')
def files():
    fill, pubs = File.list(current_user)
    try:
        f = [(url_for('.showf', fn=enfn(f)), f, u) for f, u in fill] if fill else []
        p = [(url_for('.showf', fn=enfn(f)), f, u) for f, u in pubs]
    except:
        return fill
    return render_template('file/files.html', files=f, pubs = p)


def urls(fn):
    return dict(dl=url_for('.readf', fn=fn),
                upl=url_for('.changecon', fn=fn),
                ren=url_for('.chname', fn=fn),
                show=url_for('.showf', fn=fn),
                dele=url_for('.delf', fn=fn),
                pub=url_for('.checkPub', fn=fn),
                index=url_for('.index'))


@app.route('/show/<fn>')
def showf(fn):
    f = defn(fn)
    file = fdict[f]
    if not file:
        abort(404)

    return render_template('file/show.html', f=file, urls=urls(fn))


@app.route('/dl/<fn>')
def readf(fn):
    fn = defn(fn)
    file = fdict[fn]
    rfn, fi, pub = file.info()
    fio = io.BytesIO(fi)
    rsp = mkrsp(send_file(fio, attachment_filename=rfn, as_attachment=True))
    rsp.headers['Content-Type'] = "application/octet-stream"
    rsp.headers['Content-Encoding'] = "gzip"
    rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % rfn.encode()).decode('latin-1')
    return rsp
