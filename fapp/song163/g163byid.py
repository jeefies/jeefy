import os
import re
import sys
from json import loads
import requests


cr = re.compile("<title>.*?</title>")
scr = re.compile("\s*-\s*")

# download url
download_url = "https://music.163.com/song/media/outer/url?id={}.mp3"
# detail url
detail_url = "https://music.163.com/api/song/detail/?id={0}&ids=%5B{0}%5D"
#purl = "https://music.163.com/api/playlist/detail/?id={}"

join = os.path.join


def init():
    global ses
    ses = requests.session()
    ses.headers.update({'Origin': 'https://music.163.com',
                        "Referer": "https://music.163.com/",
                        "User-Agent": ("Mozilla/5.0 (X11; Linux aarch64)"
                                       " AppleWebKit/537.36"
                                       " (KHTML, like Gecko) Chrome"
                                       "/83.0.4103.116 Safari/537.36")})
    ses.get('https://music.163.com')


def getSongById(i, save=True, savedir=None, getname = True):
    try:
        src = ses.get(download_url.format(i))
        if src.content.startswith(b'<'):
            raise NotFoundError('song not found')
        if getname:
            name_src = ses.get(detail_url.format(i))
    except NameError:
        init()
        return getSongById(i, save, savedir, getname)

    if getname:
        try:
            r = loads(name_src.text)['songs'][0]
            songn = r['name']
            
            artists = (artist['name'].replace(' ', '_').replace('-', '_') for artist in r['artists'])
            fname = songn.replace(' ', '_').replace('-', '_') +  '-' + '/'.join(artists) + '.mp3'
        except Exception as e:
            raise NotFoundError("Id %d Not found" % i)

    if save:
        if savedir is None:
            savedir = os.getcwd()
        savename = fname if getname else str(i) + '.mp3'
        with open(join(savedir, savename), 'wb') as f:
            f.writelines(src.iter_content())
        return savename
    else:
        song = songn if getname else i
        fn = fname if getname else None
        return song, fn, b''.join(src.iter_content())


def main():
    if len(sys.argv) <= 1:
        raise ValueError('No song ids')

    ids = sys.argv[1:]
    print(ids)
    init()
    for i in ids:
        print(getSongById(i))

class NotFoundError(Exception): pass

if __name__ == '__main__':
    main()
