#flask_script 使用命令行管理项目,flask_migrate 数据库迁移脚本
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from pj import app
from exts import db
from apps.cms.models import User,Role
from apps.common.models import Banner,Post

manage=Manager(app)
Migrate(app,db)
manage.add_command('db',MigrateCommand)

@manage.option('-e','--email',dest='email')
@manage.option('-u','--username',dest='username')
@manage.option('-p','--password',dest='password')
def addcmsuser(email,username,password):
    user = User(email=email,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manage.option('-n','--rolename',dest='rolename')
@manage.option('-d','--roledesc',dest='roledesc')
@manage.option('-p','--permissions',dest='permissions')
def addcmsrole(rolename,roledesc,permissions):
    r = Role(roleName=rolename,desc=roledesc,permissions=permissions)
    db.session.add(r)
    db.session.commit()

@manage.option('-uid','--user_id',dest='user_id')
@manage.option('-rid','--role_id',dest='role_id')
def useraddrole(user_id,role_id):
    u = User.query.get(user_id)
    r = Role.query.get(role_id)
    u.roles.append(r)
    db.session.commit()

@manage.command
def addpost():
    for i in range(50):
        post=Post(title='title'+str(i),content='content'+str(i),bank_id=1,user_id='rz4mWArrJfHyuD9dZA3jTm')
        db.session.add(post)
        db.session.commit()
    print('50打印完毕')



if __name__ == '__main__':
    manage.run()