import os
from app import create_app, db
from app.models import File, User, Room, Role, Article
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv("FLASK_CONFIG", 'default'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make():
    return dict(db = db, File=File, Room=Room, Role=Role, Article = Article, User = User)

@app.cli.command()
def deploy():
    upgrade()

@app.cli.command()
def crt():
    db.create_all()

if __name__ == '__main__':
        try:
            app.run('0.0.0.0', 80)
        except:
            app.run('0.0.0.0')
