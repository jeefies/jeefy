import io
import gzip
import time
from hashlib import md5
from json import dumps, loads
from threading import Thread

from markdown import markdown
from itsdangerous.url_safe import URLSafeSerializer  as Serializer
from flask import current_app, url_for

from flask_mail import Message
# from flask_login import UserMixin, current_user

from . import db, mail, loginManager

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['MAIL_SENDER'],
            recipients=[to])
    # msg.body = render_template(...)
    msg.html = render_template(template, **kwargs)
    thd = Thread(target = send_async_email, args=[current_app, msg])
    thd.start()
    return thd

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
    users = db.relationship("User", backref='role', lazy="dynamic")

    @staticmethod
    def checkRole():
        names = ['Student', 'Teacher', 'Worker', 'Other', 'Admin']
        miss = []
        for name in names:
            if not Role.query.filter_by(name=name).all():
                r = Role(name=name)
                miss.append(r)
        else:
            db.session.add_all(miss)
            db.session.commit()

        return miss

    @classmethod
    def getRole(cls, roleName):
        return cls.query.filter_by(name = roleName).first()

    def __repr__(self):
        return "<Role %r>" % (self.name)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default = False)
    birth = db.Column(db.Date)
    # it's dangerous that not to encode the password
    password = db.Column(db.String(20))
    sex = db.Column(db.Boolean)
    desc = db.Column(db.Text)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    files = db.relationship(File, backref='user', lazy="dynamic")
    rooms = db.relationship("Room", backref='user', lazy="dynamic")

    def avatar_hash(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

    def avatar(self, size=100, default='retro'):
        if not size:
            url = "https://cravatar.cn/avatar/{}?d={}"
            return url.format(self.avatar_hash(), default)

        url = "https://cravatar.cn/avatar/{}?s={}&d={}"
        return url.format(self.avatar_hash(), size, default)

    def __repr__(self):
        return "<User %r e-at %r>" % (self.name, self.email)

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            di = s.loads(token)
        except:
            return False

        if di['name'] == self.name and di['sec'] == self.password:
            return True
        return False

    def json(self):
        # male for boy
        info = dict(name = self.name,
                    email = self.email,
                    sex = "男" if self.sex else "女",
                    role = self.role.name,
                    description = self.desc,
                    avatar = self.avatar,
                    url = "/user/%r" % self.name)
        # print(info)
        return info

    def mkd(self):
        if self.desc:
            return markdown(self.desc), True
        else:
            return 'Err... The user is too lazy that left no descriptions', False

    def gender(self):
        return ("Male" if self.sex else "Female")

    @classmethod
    def indexByName(self, name):
        return self.query.filter_by(name = name).first()

    @classmethod
    def indexByEmail(self, email):
        return self.query.filter_by(email = email).first()

loginManager.set_user_index_class(User)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    lines = db.Column(db.LargeBinary)
    linenu = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def readlines(self, size=None, loads = True):
        if not self.lines:
            return ()

        l = lambda x:loads(x.decode())
        if loads:
            return (l(i) for i in self.lines.split(b'\x00'))
        return self.lines.split(b'\x00')
    
    def getline(self, count):
        if not self.lines:
            return b''
        s = 0
        for i in range(count - 1):
            s = self.lines.index(b'\x00', s)
            
        se = self.lines.index(b'\x00', s)
        return self.lines[s + 1:se]

    def addline(self, val):
        val['id'] = self.linenu
        val['time'] = time.time()
        b = dumps(val).encode()
        self.lines = b + b'\x00' + self.lines if self.lines else b
        self.linenu += 1
        db.session.add(self)
        db.session.commit()
        return b.decode()

    def reset(self):
        self.lines = b''
        db.session.add(self)
        db.session.commit()

    def url(self):
        return url_for('room.room_', roomn=self.name)
    
    def url2(self):
        return url_for('room2.jump', room = self.name)

    def __repr__(self):
        return "<Room %r>" % self.name
