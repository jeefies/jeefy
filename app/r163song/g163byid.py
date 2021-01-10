import os
import re
import sys
import requests


cr = re.compile("<title>.*?</title>")
scr = re.compile("\s*-\s*")

durl = "https://music.163.com/song/media/outer/url?id={}.mp3"
surl = "https://music.163.com/song?id={}"

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


def getSongById(i, save=True, savedir=None, verbose=False, gn = True):
    try:
        if verbose:
            print('song content getting')
        sr = ses.get(durl.format(i))
        if verbose: print('song name getting')
        if gn:
            nr = ses.get(surl.format(i))
            if verbose: print('get all ok!')
    except NameError:
        init()
        if verbose: print('inited! again!')
        return getSongById(i, save, savedir, verbose)

    if gn:
        r = cr.search(nr.text[:10000])
        if verbose: print('searching song name')
        s, e = r.start(), r.end()
        text = nr.text[s + 7: e - 8]
        li = scr.split(text)
        song, auth = li[0:2]
        song = song.replace(' ', '_')
        if verbose: print('concating song file name ', end="", flush=True)
        fname = song + '-' + auth + '.mp3'
        if verbose: print(fname)
    if save:
        if savedir is None:
            savedir = os.getcwd()
        savename = song + '-' + auth + '.mp3' if gn else str(i) + '.mp3'
        with open(join(savedir, savename), 'wb') as f:
            f.writelines(sr.iter_content())
        return savename
    else:
        if verbose: print('returning content')
        song = song if gn else i
        fn = fname if gn else None
        return song, fn, b''.join(sr.iter_content())


def main():
    if len(sys.argv) <= 1:
        raise ValueError('No song ids')

    ids = sys.argv[1:]
    print(ids)
    init()
    for i in ids:
        print(getSongById(i))


if __name__ == '__main__':
    main()
