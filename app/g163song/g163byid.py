import os
import re
import sys
from json import loads
import requests


cr = re.compile("<title>.*?</title>")
scr = re.compile("\s*-\s*")

durl = "https://music.163.com/song/media/outer/url?id={}.mp3"
jurl = "https://music.163.com/api/song/detail/?id={0}&ids=%5B{0}%5D"

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


def getSongById(i, save=True, savedir=None, gn = True):
    try:
        sr = ses.get(durl.format(i))
        if gn:
            nr = ses.get(jurl.format(i))
    except NameError:
        init()
        return getSongById(i, save, savedir, gn)

    if gn:
        try:
            r = loads(nr.text)['songs'][0]
            songn = r['name'].replace(' ', '_').replace('-', '_')
            artists = r['artists']
            for art in artists:
                songn += '-'
                songn += art['name'].replace(' ', '_').replace('-', '_')
            fname = songn + '.mp3'
        except:
            raise NotFoundError("Id %d Not found" % i)
    if save:
        if savedir is None:
            savedir = os.getcwd()
        savename = fname if gn else str(i) + '.mp3'
        with open(join(savedir, savename), 'wb') as f:
            f.writelines(sr.iter_content())
        return savename
    else:
        song = songn if gn else i
        fn = fname if gn else None
        return song, fn, b''.join(sr.iter_content())


def main():
    if len(sys.argv) <= 1:
        raise ValueError('No song ids')

    ids = sys.argv[1:]
    print(ids)
    init()
    for i in ids:
        print(getSongById(i, verbose = 1))

class NotFoundError(Exception): pass

if __name__ == '__main__':
    main()
