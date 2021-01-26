from ..models import db, File

class Fdict(dict):
    def __getitem__(self, index):
        return super().get(index, self.fromName(index))

    def __setitem__(self, key, value):
        o = self.get(key, None)
        if o is None or (isinstance(o, File) and o != value):
            db.session.add(value)
            db.session.commit()
            super().__setitem__(key, value)
            return True
        return False

    def pop(self, key):
        try:
            f = super().pop(key)
        except:
            return None
        db.session.delete(f)
        db.session.commit()
        return f

    def __delitem__(self, key):
        return self.pop(key)

    def fromName(self, name):
        f = File.query.filter_by(fn = name).first()
        if f:
            self[name] = f
        return f