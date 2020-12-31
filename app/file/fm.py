import io
import os
import gzip
import copy
import time
import zipfile

from ..paths import FILEPATH

_SFN = os.path.join(FILEPATH, 'zipfile.zip')

def toZipIO(fn, bs):
    bf = io.BytesIO()
    fn += '.gz'
    with gzip.GzipFile(fn, 'w', fileobj=bf) as f:
        f.write(bs)
    return fn, io.BytesIO(bf.getvalue())

    

class BufferZipFile:
    def __init__(self):
        self.bio = io.BytesIO()
        self.init()
        globals()['CON'] = b''
        self.inti = time.time()

    def check(self):
        if time.time() - self.inti > 3:
            print('flushing...again')
            self.flush()
            self.inti = time.time()

    def init(self):
        try:
            print('reading for file...', end='', flush=True)
            with io.open(_SFN, 'rb') as f:
                bs = f.read()
            print('success')
            if bs:
                opt = 'a'
            else:
                opt = 'w'
        except Exception as e:
            print('failed:', e)
            bs = b''
            opt = 'w'
        self.bio = io.BytesIO(bs)
        self.file = zipfile.ZipFile(self.bio, opt, zipfile.ZIP_STORED)

    def list(self):
        self.check()
        return self.file.filelist

    def listname(self):
        self.check()
        return [f.filename for f in self.file.filelist]

    def write(self, fn, ctx):
        if not fn in self.listname():
            self.file.writestr(fn, ctx)
        else:
            b = io.BytesIO()
            zf = zipfile.ZipFile(b, 'w', zipfile.ZIP_STORED)
            for f in self.listname():
                if f != fn:
                    zf.write(self.read(f))
                else:
                    r = zf.writestr(fn, ctx)
            del self.file, self.bio
            self.bio = b
            self.file = zf
        self.check()

    def read(self, fn):
        self.check()
        return toZipIO(fn, self.file.read(fn))

    def wtfwrite(self, data):
        f = io.BytesIO()
        data.save(f)
        return self.write(data.filename, f.getvalue())

    def __del__(self):
        self.file.close()
        self.bio.close()

    def flush(self):
        try:
            with io.open(_SFN, 'wb') as f:
                self.file.close()
                con = self.bio.getvalue()
                f.write(con)
            self.file = zipfile.ZipFile(self.bio, 'a', zipfile.ZIP_STORED) 
        except Exception as e:
            print('flush failed', e)
            return

Files = BufferZipFile()
