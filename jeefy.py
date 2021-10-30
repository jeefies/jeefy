#!/usr/bin/env python3

import os
from app import create_app, db
from app.models import File, User, Room, Role, Article
from flask_migrate import Migrate, upgrade, init


app = create_app(os.getenv("FLASK_CONFIG", 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make():
    return dict(db=db, File=File, Room=Room,
                Role=Role, Article=Article, User=User)


@app.cli.command()
def deploy():
    try:
        Role.checkRole()
        upgrade()
    except:
        try:
            upgrade()
        except:
            init()
        Role.checkRole()


@app.cli.command()
def reset():
    db.drop_all()
    _create()

@app.cli.command()
def initdb():
    _create(0)

@app.cli.command()
def create():
    _create()

def _create(crt = True):
    if crt:
        db.create_all()
    allr = Role.checkRole()
    admin = allr[1]
    u1 = User(email = 'jeefy163@163.com', name = 'jeefy', password = 12345678, sex=0, role=admin)
    u2 = User(email = 'jeefy_test@126.com', name = 'ipad', password = 12345678, sex=0, role=admin)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()


if __name__ == '__main__':
    try:
        app.run('0.0.0.0', 80)
    except:
        try:
            app.run('0.0.0.0')
        except:
            app.run("0.0.0.0", 5050)
