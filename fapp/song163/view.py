"""
views:
    / (index): Main page to get the song by id
    /get?Id=... (gets): get the song by id, return a file (type='audio/mp3')
"""
import io
import gzip

from .bp import song
from ..imps import *
# The main file to get the song
from .g163byid import getSongById, getSongName, NotFoundError
from .g163byid import init as init_song163

from functools import lru_cache

# init_song163()

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
        flash("错误的音乐ID")
        return redirect(url_for('.index'))

    try:
        return get(sid)
    except NotFoundError:
        # No such song according to the id
        flash("没有找到这首歌！")
        return redirect(url_for('.index'))

def get(sid):
    # song-name file-name bytes-source
    songn, filen, src = getSongById(sid, False, getname = request.values.get("raw") != "raw")
    # print("Got it!")
    file = io.BytesIO(src)
    file.seek(0)

    as_attachment = True
    if request.values.get("raw") == "raw":
        as_attachment = False
    return send_file(file, "audio.mp3", True, filen, filen)

@song.route('/name', methods=["GET", "POST"])
def getname():
    try:
        sid = int(request.values.get("id"))
    except:
        return jsonify({'status': False, 'reason': "没有给定的音乐ID"})

    try:
        songn = getSongName(sid)
    except NotFoundError:
        return jsonify({'status': False, 'reason': f"没有找到ID为{sid}的音乐"})

    print("song name", songn)
    return jsonify({'status': True, 'songname': songn})
