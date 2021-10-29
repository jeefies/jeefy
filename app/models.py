import io
import gzip
from hashlib import md5
from json import dumps, loads
from markdown import markdown

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from flask_login import UserMixin, current_user

from . import db, loginmanager


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    fn = db.Column(db.String(32), unique=True, nullable=False)
    ct = db.Column(db.LargeBinary)
    pub = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def ctx(self):
        return gzip.decompress(self.ct)

    def text(self):
        try:
            return gzip.decompress(self.ct).decode(), True
        except:
            return gzip.decompress(self.ct), False

    @ctx.setter
    def ctx(self, val):
        b = io.BytesIO()
        with gzip.GzipFile(self.fn, 'w', 6, b) as f:
            f.write(val)
        self.ct = b.getvalue()

    def info(self):
        return (self.fn, self.ct, self.pub)

    @classmethod
    def add_form_data(cls, data, puc):
        b = io.BytesIO()
        data.save(b)
        fn = data.filename
        fr = cls.query.filter_by(fn = fn)
        if fr.first():
            return None
        else:
            f = File(fn=data.filename)
            f.ctx = b.getvalue()
            f.pub = puc
        return f

    @classmethod
    def list(cls, user):
        try:
            own = set(cls.query.filter_by(user=user).all())
        except:
            own = set()
        pucf = set(cls.query.filter_by(pub=True).all())
        pucf.update(own)
        f = lambda x : (x.fn, x.user)
        return map(f, own), map(f, own ^ pucf)

    def isOwn(self):
        return self.user == current_user


    def __repr__(self):
        return "<File %r to %r.gz>" % self.fn


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), unique=True)
    permission = db.Column(db.SmallInteger)
    users = db.relationship("User", backref='role', lazy="dynamic")

    def addper(self, val):
        self.permission |= val
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def checkRole():
        names = [('Student', 0b111), ('Admin', 0b1111), ('Teacher', 0b111), ('Other', 0b111),
                 ('Worker', 0b111), ('Visitor', 0b11)]
        miss = []
        for name, per in names:
            if not Role.query.filter_by(name=name).all():
                r = Role(name=name, permission=per)
                miss.append(r)
        else:
            db.session.add_all(miss)
            db.session.commit()

        return miss

    def __repr__(self):
        return "<Role %r for %r>" % (self.name, self.permission)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    birth = db.Column(db.Date)
    # it's dangerous that not to encode the password
    password = db.Column(db.String(20))
    sex = db.Column(db.SmallInteger)
    desc = db.Column(db.Text)
    avater_hash = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    files = db.relationship(File, backref='user', lazy="dynamic")
    articles = db.relationship("Article", backref='user', lazy="dynamic")
    rooms = db.relationship("Room", backref='user', lazy="dynamic")

    # permission definations
    NONE = 0
    READ = 1 << 0
    WRITE = 1 << 1
    MODIFY = 1 << 2
    ADMIN = 1 << 3

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avater_hash is None:
            self.avater_hash = self.gravatar_hash()

    def gravatar_hash(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = "https://secure.gravatar.com/avatar/{}?s={}&d={}&r={}"
        return url.format(self.avater_hash, size, default, rating)

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
            di = s.loads(token.encode())
        except:
            return False

        if di['name'] == self.name and di['sec'] == self.password:
            return True
        return False

    def generate_token(self, exp):
        s = Serializer(current_app.config["SECRET_KEY"], exp)
        di = dict(name=self.name, sec=self.password)
        return s.dumps(di).decode()

    def json(self):
        # male for boy
        return dict(name=self.name,
                    sex="male" if self.sex else "female",
                    role=self.role.name,
                    permission=self.permission,
                    description=self.desc,
                    url="/user/%r" % self.id)

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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    introduce = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def html(self):
        return markdown(self.content)

    def json(self):
        return dict(title=self.title,
                    author=self.user.name,
                    introduce=self.introduce,
                    content=self.content)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    lines = db.Column(db.LargeBinary)
    ius = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def readlines(self, size=None, loads = True):
        if not self.lines:
            return ()

        l = lambda x:loads(x.decode())
        if loads:
            return (l(i) for i in self.lines.split(b'\x00'))
        return self.lines.split(b'\x00')

    def addline(self, val):
        val['gravatar'] = current_user.gravatar(50)
        b = dumps(val).encode()
        self.lines = b + b'\x00' + self.lines if self.lines else b
        db.session.add(self)
        db.session.commit()
        return b.decode()

    def reset(self):
        self.lines = b''
        db.session.add(self)
        db.session.commit()

    def url(self):
        return url_for('room.room_', roomn=self.name)

    def __repr__(self):
        return "<Room %r>" % self.name
