import base64
from functools import lru_cache

from ..models import Room, db


@lru_cache()
def b16e(b):
    return base64.b16encode(b.encode()).decode()

@lru_cache()
def b16d(b):
    return base64.b16decode(b.encode()).decode()

@lru_cache()
def tod(b):
    try:
        return b16d(b)
    except:
        return b

class Rdict:
    _ins = None
    enc = staticmethod(b16e)
    def __new__(self):
        if not self._ins:
            self._ins = super().__new__(self)
        return self._ins

    def __init__(self):
        pass

    def get(self, index):
        n = tod(index)
        r = Room.query.filter_by(name = n).first()
        return r
    
    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, room):
        if self[index] != room:
            db.session.add(room)
            db.session.commit()

    def __delitem__(self, index):
        return self.pop(index)

    def pop(self, index):
        r = self.get(index)
        db.session.delete(r)
        db.session.commit()
        return r

    def add(self, room):
        db.session.add(room)
        db.session.commit()
