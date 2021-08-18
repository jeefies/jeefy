"""
views:
    / (index): List all the rooms
    /room/<room> (room_): redirect to chatting
    /new (new): regist a new room and redirect to chatting
    /rom/<u> (chatting): main chatting page
    /rom/<u>/data (recv_data): where the line submit to
    /rom/<u>/evd (event_data): event-stream data with Work class
    /romd/<u> (droom): delete the room and redirect to index
    /romr/<u> (reset): reset the room contents
"""
import time
from json import loads, dumps
from functools import lru_cache

from ..imps import *
from ..models import Room
from ..worker import Work, Worker
from .. import db
from .rdict import Rdict

from .bp import room

WORKS = {}
rdict = Rdict()

@room.route('/new')
@login_required
def new():
    n = req.args.get('name')
    if n:
        if rdict[n]:
            flash("The name is already in used! Please change another one")
            return redirect(url_for('.new'))
        r = Room(name = n, user = current_user)
        rdict.add(r)
        return redirect(url_for('.room_', roomn = n))
    return render_template('room/new.html')

@room.route('/room/<roomn>')
@login_required
def room_(roomn):
    ju = rdict.enc(roomn)
    return redirect(url_for('.chatting', u = ju))

@room.route('/rom/<u>', methods=['post', 'get'])
@login_required
def chatting(u):
    r = rdict[u]
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    return render_template('room/chat.html', room = r, u = url_for('.jget', u = u), _u = u)

@room.route('/rom/<u>/data', methods=['POST'])
def recv_data(u):
    r =rdict[u]
    di = dict(ctx = req.values.get('line'),
        user = current_user.name,
        time = time.time())
    sj = r.addline(di)
    j = jsonify(sj)
    getwork(u).add(sj.encode())
    return j

@room.route('/rom/<u>/evd')
def event_data(u):
    rsp = Rsp(WebWorker(getwork(u)).iter(), mimetype="text/event-stream")
    return rsp

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
    r = rdict[u]
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    return dumps(tuple(r.readlines(n)))

@room.route('/romd/<u>')
@login_required
def droom(u):
    r = rdict[u]
    w = getwork(u)
    w.call('send', 'destroy')
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if not r.user == current_user:
        flash('You have no access')
        return redirect(url_for('.index'))
    w.destroy()
    rdict.pop(u)
    flash('Delete success!')
    return redirect(url_for('.index'))

@room.route('/romr/<u>')
@login_required
def reset(u):
    r = rdict[u]
    w = getwork(u)
    w.call('send', 'reset')
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if not r.user == current_user:
        flash('You have no access')
        return redirect(url_for('.index'))
    r.reset()
    w.reset()
    flash('You have Clear All Chatting Histories')
    return redirect(url_for('.chatting', u = u))


class WebWorker(Worker):
    def tob(self, ctx):
        if isinstance(ctx, (bytes, bytearray)):
            return ctx
        elif isinstance(ctx, str):
            return ctx.encode()
        return str(ctx).encode()

    def analyze(self, ctx):
        ctx = self.tob(ctx)
        return b'data:'+ ctx+ b'\n\n'

def getwork(u):
    if u not in WORKS:
        r = rdict[u]
        w = WORKS[u] = Work(u)
        for l in r.readlines(loads = False):
            w.add(l)
    return WORKS[u]
