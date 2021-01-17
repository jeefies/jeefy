import zlib
import time
import codecs
import base64
from json import loads, dumps
from functools import lru_cache

from ..imps import *
from ..models import Room
from .. import db

from .bp import room

@room.route('/new')
@login_required
def new():
    n = req.args.get('name')
    if n:
        if Room.query.filter_by(name = n).first():
            flash("The name is already in used!Please change another one")
            return redirect(url_for('.new'))
        r = Room(name = n, user = current_user)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('.room_', roomn = n))
    return render_template('room/new.html')

def b16e(b):
    return base64.b16encode(b.encode()).decode()

def b16d(b):
    return base64.b16decode(b.encode()).decode()

@room.route('/room/<roomn>')
@login_required
def room_(roomn):
    ju = b16e(roomn)
    return redirect(url_for('.chatting', u = ju))

@room.route('/rom/<u>', methods=['post', 'get'])
@login_required
def chatting(u):
    r = get_room(u)
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if req.method == "POST":
        ctx = req.values.get('line')
        if ctx:
            di = {'ctx': ctx, 'user': current_user.name,
                    'time': time.time()}
            print('add +1')
            r.addline(di)
            print(r.readlines())
        return redirect(url_for('.chatting', u = u))
    return render_template('room/chat.html', room = r, u = url_for('.jget', u = u), _u = u)

def get_room(u):
    try:
        n = b16d(u)
    except:
        return None
    return Room.query.filter_by(name = n).first()

@room.route('/')
def index():
    rooms = Room.query.all()
    return render_template('room/index.html', rooms = rooms)

@room.route('/romj/<u>')
@login_required
def jget(u):
    n = req.args.get('lines')
    if n:
        n = int(n)
    r = get_room(u)
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    return dumps(tuple(r.readlines(n)))

@room.route('/romd/<u>')
@login_required
def droom(u):
    r = get_room(u)
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if not r.user == current_user:
        flash('You have no access')
        return redirect(url_for('.index'))
    db.session.delete(r)
    db.session.commit()
    flash('Delete success!')
    return redirect(url_for('.index'))

@room.route('/romr/<u>')
@login_required
def reset(u):
    r = get_room(u)
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if not r.user == current_user:
        flash('You have no access')
        return redirect(url_for('.index'))
    r.reset()
    flash('Reset success!')
    return redirect(url_for('.chatting', u = u))
