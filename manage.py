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

#测试数据库初始化
@manager.command
def datainit():
    from app.models import Role,User,Post
    print ("Role init")
    User.add_self_follows()
    Role.insert_role()
    print ("User and Post generate")
    User.generate_fake(100)
    Post.generate_fake(100)
    wen=User.query.filter_by(username='wen').first()
    if not wen:
        print ("make wen in admin")
        wen=User(username='wen',email='zhangjinwei94@163.com',password='123456',confirmed=True)
        wen.role=Role.query.filter_by(permissions=0xff).first()
        db.session.add(wen)
        db.session.commit()
    else :
        print ("User(wen) already in data")
    print ("all_data readly now")


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    #upgrade()

    # create user roles
    Role.insert_role()




if __name__ == '__main__':
    manager.run()