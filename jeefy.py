#!/usr/bin/env python3

import os
from fapp import create_app, db
from fapp.models import File, User, Room, Role
from flask_migrate import Migrate, upgrade, init


app = create_app(os.getenv("FLASK_CONFIG", 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make():
    return dict(db=db, File=File, Room=Room,
                Role=Role, User=User)


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
def resetDB():
    db.drop_all()
    _create()

@app.cli.command()
def initDB():
    _create(0)

@app.cli.command()
def createDB():
    _create()

def _create(crt = True):
    if crt:
        db.create_all()
    allr = Role.checkRole()
    admin = Role.query.filter_by(name = 'Admin').first()
    u = User(email = 'jeefy163@163.com', name = 'jeefy', password = 12345678, sex = True, role = admin)
    db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    try:
        app.run('0.0.0.0', 80)
    except:
        try:
            app.run('0.0.0.0')
        except:
            app.run("0.0.0.0", 5050)
