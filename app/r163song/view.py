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
    print('song getting')
    sn, fn, sc = getSongById(sid, False, verbose=True)
    print("Got it!")
    """
    b = io.BytesIO()
    print(sn)
    with gzip.GzipFile(fn, 'w', fileobj = b) as f:
        f.write(sc)
    """
    rsp = mkrsp(sc)
    rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % (fn.encode('utf-8'))).decode('latin-1')
    rsp.headers['Content-Type'] = "application/octet-stream"
    return rsp

@song.route('/raw')
def raw():
    return rawm()

@lru_cache(None)
def rawm():
    try:
        sid = int(req.args.get('Id'))
    except:
        return "Error Song Id!"
    _, _, sc = getSongById(sid, False, gn=False)
    rsp = mkrsp(sc)
    rsp.headers['Content-Type'] = "audio/mp3"
    return rsp

