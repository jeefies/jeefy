"""
views:
    / (index): Main page to get the song by id
    /get?Id=... (gets): get the song by id, return a file (type='octet-stream')
    /raw?Id=... (raws): return the raw song (type='audio/mp3')
"""
import io
import gzip

from .bp import song
from ..imps import *
# The main file to get the song
from .g163byid import init, getSongById, NotFoundError

from functools import lru_cache


@song.route('/')
def index():
    return render_template('r163song/index.html')

"""
@song.route('/playlist')
def playlists():
    try:
        sid = int(req.args.get("Id"))
    except ValueError:
        return "Error Song Id!"
    try:
        return playlist(sid)
    except NotFoundError:
        flash("Error playlist Id!")
    return redirect(url_for('.index'))
"""


@song.route('/get')
def gets():
    try:
        # like raws, get the song id by get method
        sid = int(req.args.get('Id'))
    except:
        # if the id is not plain digits, return a error message.
        return "Error Song Id!"
    try:
        return get(sid)
    except NotFoundError:
        # No such song according to the id
        flash("Error song Id!")
        return redirect(url_for('.index'))

@lru_cache()
def get(sid):
    # song-name file-name bytes-source
    sn, fn, sc = getSongById(sid, False)

    print("Got it!")
    rsp = mkrsp(sc)
    # let browser know it's the file to download
    rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % (fn.encode('utf-8'))).decode('latin-1')
    rsp.headers['Content-Type'] = "application/octet-stream"
    return rsp

@song.route('/raw')
def raws():
    # the same as gets
    try:
        sid = int(req.args.get('Id'))
    except ValueError:
        return "Error Song Id!"
    try:
        return rawm(sid)
    except NotFoundError:
        flash("Error song Id!")
        return redirect(url_for('.index'))

@lru_cache()
def raw(sid):
    # use _ to let the place empty, need only source
    _, _, sc = getSongById(sid, False, gn=False)
    rsp = mkrsp(sc)
    rsp.headers['Content-Type'] = "audio/mp3"
    return rsp
