import base64

from ..models import Room, db


def b16e(b):
    return base64.b16encode(b.encode()).decode()

def b16d(b):
    return base64.b16decode(b.encode()).decode()

class _bdict:
    _ins = None
    def __new__(self):
        if not self._ins:
            self._ins = super().__new__(self)
        return self._ins

    def __init__(self):
        self.nb = dict()

    def get(self, index, e):
        n = self.nb.get(index, None)
        if not n:
            n = self.nb[n] = b16d(index)
        r = Room.query.filter_by(name = n).first()
        return r if r else e
    
    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, room):
        self.nb[index] = room.name

    def pop(self, index):
        r = self.get(index)
        self.nb.pop(index)
        return r

class Rdict:
    _ins = None
    enc = staticmethod(b16e)
    def __new__(self):
        if not self._ins:
            self._ins = super().__new__(self)
        return self._ins

    def __init__(self):
        self.nd = _ndict()
        self.bd = _bdict()

    def get(self, index, e):
        print('get', self.nd, self.bd)
        return self.bd.get(index, self.nd.get(index, e))

    def __getitem__(self, index):
        r = self.get(index, None)
        if r:
            return r
        u = Room.query.filter_by(name = b16d(index)).first()
        if u:
            self.add(u)
            return u

    def add(self, room):
        o = self.nd.get(room.name, None)
        if o is None or o != room:
            db.session.add(room)
            db.session.commit()
        self.bd[b16e(room.name)] = self.nd[room.name] = room
        print('add', self.bd, self.nd)
        return room

    def __setitem__(self, index, room):
        return self.add(room)

    def pop(self, name, commit = True):
        self.nd.pop(name)
        r = self.bd.pop(b16e(name))
        db.session.delete(r)
        if commit:
            db.session.commit()
        return r

    def popu(self, base, commit = True):
        r = self.bd.pop(base)
        self.nd.pop(r.name)
        db.session.delete(r)
        if commit:
            db.session.commit()
        return r

    def __delitem__(self, index):
        return self.popu(index)
