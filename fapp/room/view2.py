"""
view:
    / (index)
    /room/<room> (jump)
    /r/<u> (room)
    /r/<u>/data (pdata)
    /r/<u>/data/length (ldata)
    /r/<u>/data/<int:line> (idata)
    /new (new): regist a new room and redirect to chatting
"""

from json import loads, dumps

from ..imps import *
from ..models import Room
from .. import db
from .rdict import Rdict

from .bp import room2 as room

rdict = Rdict()

@room.route('/new')
@login_required
def new():
    n = req.args.get('name')
    if n:
        if rdict[n]:
            flash("The name is already in used! Please change another one")
            return redirect(url_for('.new'))
        r = Room(name = n, user = current_user,  linenu = 0)
        rdict.add(r)
        return redirect(url_for('.jump', room = n))
    return render_template('room/new.html')

@room.route('/')
def index():
    rooms = Room.query.all()
    return render_template('room/index2.html', rooms = rooms)

@room.route('/room/<room>')
@login_required
def jump(room):
    ju = rdict.enc(room)
    return redirect(url_for('.chatting', u = ju))

@room.route('/r/<u>')
@login_required
def chatting(u):
    r = rdict[u]
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    return render_template('room/chat2.html', roomurl = req.path, room = r)

@room.route('/r/<u>/data', methods="POST GET".split())
@login_required
def pdata(u):
    r = rdict[u]
    if req.method == 'GET':
        return jsonify(r.getlines(loads=False))
    elif req.method == "POST":
        data = req.values.get("data")
        print(req.values, data)
        name = current_user.name
        result = r.addline(dict(ctx=data, name=name))
        return result
    
@room.route('/r/<u>/data/length')
@login_required
def ldata(u):
    return str(rdict[u].linenu)

@room.route('/r/<u>/data/<int:id>')
@login_required
def idata(u, id):
    return rdict[u].getline(id)

@room.route('/delete/<u>')
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

@room.route('/reset/<u>')
@login_required
def reset(u):
    r = rdict[u]
    if not r:
        flash('no such room')
        return redirect(url_for('.index'))
    if not r.user == current_user:
        flash('You have no access')
        return redirect(url_for('.index'))
    r.reset()
    flash('You have Clear All Chatting Histories')
    return redirect(url_for('.chatting', u = u))
