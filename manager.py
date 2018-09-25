#flask_script 使用命令行管理项目,flask_migrate 数据库迁移脚本
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from pj import app
from exts import db
from apps.cms.models import User

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

if __name__ == '__main__':
    manage.run()
