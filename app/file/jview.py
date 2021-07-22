"""
All return json
views:
    /cc/<fn>(changecon): 
        method=POST only, Change a file's content("ctx")
    /cn/<fn>(chname):
        method=POST only, Change a file's name("name")
    /del/<fn>(delf):
        method=GET, delete a file content
    /puc/<fn>(checkPub):
        method=GET, check if a file is public
"""
from base64 import b16encode as b16en
from base64 import b16decode as b16de

from json import dumps as jdumps

from ..imps import *
from .bp import mfile as app
from ..models import File
from .fdict import Fdict


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


@app.route('/cc/<fn>', methods=["POST"])
def changecon(fn):
    try:
        ctx = req.values.get('ctx')
        n = defn(fn)
        file = File.query.filter_by(fn=n).first_or_404()
        file.ctx = ctx.encode()
        db.session.add(file)
        db.session.commit()
        return jsonify({'code': 200, 'success': True})
    except Exception as e:
        j = jsonify({'code': 500, 'success': False, 'error': str(e)})
        j.status_code = 500
        return j


@app.route('/cn/<fn>', methods=["POST"])
def chname(fn):
    newn = req.values.get('name')
    n = defn(fn)
    if newn == n:
        return jsonify({'code': 200, 'success': True, 'reload': False})
    file = File.query.filter_by(fn=n).first_or_404()
    file.fn = newn
    file.ctx = file.ctx
    db.session.add(file)
    db.session.commit()
    return jsonify({'code': 200, 'success': True, 
        'reload': True, 'url': url_for('.showf', fn=enfn(newn))})
        
@app.route('/del/<fn>')
def delf(fn):
    fn = defn(fn)
    file = fdict.pop(fn)
    if not file:
        abort(404)
    fn, ct = file.info()
    di = dict(filename=fn,
              warn=("content is a bytes array. "
                    "After turning into python list, "
                    "use bytes(thelist) to convert it back to bytes"),
              code=200,
              content=jdumps(tuple(ct)))
    rsp = mkrsp(jdumps(di, indent=4))
    rsp.headers['Content-Type'] = "application/json"
    return rsp

@app.route("/puc/<fn>")
def checkPub(fn):
    f = enfn(fn)
    file = fdict[f]
    if not file:
        j = jsonify({'code': 404, "error": "File Not Found"})
        j.status_code = 404
        return j
    if req.method == "POST" and req.values.get("method", '') == "Change Pub":
        file.pub = not file.pub
        fdict[f] = file
        return jsonify({'code': 200, "public": file.pub})
    elif req.method == "GET":
        return jsonify({"code": 200, "public": file.pub})
