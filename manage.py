#!/use/bin/env python
# -*- coding=utf-8 -*-
import os
COV = None
if os.environ.get('FLASKY_CONVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Permission, Post, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    pass

@manager.command
def profile(length=25, profile_dir=None):
    '''在请求分析器的监视下运行程序'''
    pass


@manager.command
def deploy():
    pass


if __name__ == '__main__':
    manager.run()