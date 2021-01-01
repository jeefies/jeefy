import io
import gzip

from . import db

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key = True)
    fn = db.Column(db.String(32), unique = True)
    ct = db.Column(db.LargeBinary)

    @property
    def ctx(self):
        return gzip.decompress(self.ct)

    @ctx.setter
    def ctx(self, val):
        self.ct = gzip.compress(val)

    def info(self):
        return (self.fn + '.gz', self.ct)
    
    @classmethod
    def add_form_data(cls, data):
        b = io.BytesIO()
        data.save(b)
        fn = data.filename
        fr = cls.query.filter_by(fn = fn)
        if fr.first():
            f = fr.first()
        else:
            f = File(fn = data.filename)
        f.ctx = b.getvalue()
        return f

    @classmethod
    def list(self):
        return map(lambda x: x.fn, self.query.all())

    def __repr__(self):
        return "<File %r to %r.gz>" % self.fn


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(32), unique=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String(10))
