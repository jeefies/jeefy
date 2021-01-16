import io
import gzip

from .bp import song
from ..imps import *
from .g163byid import init, getSongById
from functools import lru_cache

@song.route('/')
def index():
    return render_template('r163song/index.html')

@song.route('/get')
def gets():
    try:
        sid = int(req.args.get('Id'))
    except:
        return "Error Song Id!"
    return get(sid)

@lru_cache()
def get(sid):
    sn, fn, sc = getSongById(sid, False)
    print("Got it!")
    rsp = mkrsp(sc)
    rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % (fn.encode('utf-8'))).decode('latin-1')
    rsp.headers['Content-Type'] = "application/octet-stream"
    return rsp

@song.route('/raw')
def raw():
    try:
        sid = int(req.args.get('Id'))
    except:
        return "Error Song Id!"
    return rawm(sid)

@lru_cache()
def rawm(sid):
    _, _, sc = getSongById(sid, False, gn=False)
    rsp = mkrsp(sc)
    rsp.headers['Content-Type'] = "audio/mp3"
    return rsp

