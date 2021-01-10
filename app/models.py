import io
import gzip
from markdown import markdown

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, abort
from flask_login import UserMixin, current_user

from . import db, loginmanager

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key = True)
    fn = db.Column(db.String(32), unique = True, nullable = False)
    ct = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def ctx(self):
        return gzip.decompress(self.ct)

    @ctx.setter
    def ctx(self, val):
        b = io.BytesIO()
        with gzip.GzipFile(self.fn, 'w', 6, b) as f:
            f.write(val)
        self.ct = b.getvalue()

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
    def list(self, user):
        try:
            return map(lambda x: (x.fn, x.user), self.query.filter_by(user = user).all())
        except:
            return loginmanager.unauthorized()

    def __repr__(self):
        return "<File %r to %r.gz>" % self.fn

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(12), unique = True)
    permission = db.Column(db.SmallInteger)
    users = db.relationship("User", backref = 'role', lazy = "dynamic")
    
    def addper(self, val):
        self.permission |= val
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def checkRole():
        names = [('Student', 0b111), ('Admin', 0b1111), ('Teacher', 0b111), ('Other', 0b111)]
        miss = []
        for name, per in names:
            if not Role.query.filter_by(name = name).all():
                r = Role(name = name, permission = per)
                miss.append(r)
        else:
            db.session.add_all(miss)
            db.session.commit()        


    def __repr__(self):
        return "<Role %r for %r>" % (self.name, self.permission)


NONE = 0
READ = 1 << 0
WRITE = 1 << 1
MODIFY = 1 << 2
ADMIN = 1 << 3

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(32), unique=True, nullable = False)
    birth = db.Column(db.Date)
    password = db.Column(db.String(20))
    #locale = db.Column(db.String(32))
    # male for boy 0, female for girl 1
    sex = db.Column(db.SmallInteger)
    desc = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    files = db.relationship(File, backref = 'user', lazy = "dynamic")
    articles = db.relationship("Article", backref = 'user', lazy = "dynamic")
    rooms = db.relationship("Room", backref = 'user', lazy = "dynamic")

    def __repr__(self):
        return "<User %r e-at %r>" % (self.name, self.email)

    def can(self, per):
        return per & self.role.permission

    @property
    def permission(self):
        return self.role.permission

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            di = s.loads(exp.encode())
        except:
            return False

        if di['name'] == self.name and di['sec'] == self.password:
            return True
        return False

    def generate_token(self, exp):
        s = Serializer(current_app.config["SECRET_KEY"], exp)
        di = dict(name = self.name, sec = self.password)
        return s.dumps(di).decode()

    def json(self):
        # male for boy
        return dict(name = self.name,
                sex = "male" if self.sex else "female",
                role = self.role.name,
                permission = self.permission,
                description = self.desc,
                url = "/user/%r" % self.id)

    def mkd(self):
        if self.desc:
            return markdown(self.desc), True
        else:
            return 'Err... The user is too lazy that left no descriptions', False

    def gender(self):
        return ("Female" if self.sex else "Male")

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), unique = True, nullable = False)
    introduce = db.Column(db.String(100))
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def html(self):
        return markdown(self.content)

    def json(self):
        return dict(title = self.title,
                author = self.user.name,
                introduce = self.introduce,
                content =  self.content)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True, nullable = False)
    lines = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def readlines(self):
        return self.lines.split('\x00')[1:]

    def addline(self, val):
        b = json.dumps(val).encode()
        self.lines += b'\x00' + b
        db.session.add(self)
        db.session.commit()

    def reset(self):
        self.lines = b''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Room %r>" % self.name
