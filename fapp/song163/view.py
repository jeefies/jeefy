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
    return render_template('song163/index.html')

"""
@song.route('/playlist')
def playlists():
    try:
        sid = int(request.args.get("Id"))
    except ValueError:
        return "Error Song Id!"
    try:
        return playlist(sid)
    except NotFoundError:
        flash("Error playlist Id!")
    return redirect(url_for('.index'))
"""


@song.route('/get', methods=["GET", "POST"])
def gets():
    try:
        # like raws, get the song id by get method
        sid = int(request.values.get('id'))
    except:
        # if the id is not plain digits, return a error message.
        print(request.values)
        flash("Error song Id!")
        return redirect(url_for('.index'))
    try:
        return get(sid)
    except NotFoundError:
        # No such song according to the id
        flash("Error song Id!")
        return redirect(url_for('.index'))

def get(sid):
    # song-name file-name bytes-source
    @lru_cache()
    def cache_get(isid):
        return getSongById(isid, False)

    songn, filen, src = cache_get(sid)

    # print("Got it!")
    file = io.BytesIO(src)
    file.seek(0)
    # rsp = make_response(sc)
    # let browser know it's the file to download
    # rsp.headers['Content-Disposition'] = (b"attachment;filename=%s" % (fn.encode('utf-8'))).decode('latin-1')
    # rsp.headers['Content-Type'] = "application/octet-stream"
    return send_file(file, "audio.mp3", True, filen, filen)

@song.route('/raw')
def raws():
    # the same as gets
    try:
        sid = int(request.values.get('id'))
    except ValueError:
        return "Error Song Id!"
    try:
        return raw(sid)
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
