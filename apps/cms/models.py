from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    _password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(30),nullable=False,unique=True)
    join_time=db.Column(db.DateTime,default=datetime.now)

    def __init__(self,password,**kwargs):
        self.password=password
        kwargs.pop('password',None)
        super(User,self).__init__(**kwargs)


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,frontpwd):
        self._password=generate_password_hash(frontpwd)

    def checkPwd(self,frontpwd):
        return check_password_hash(self._password,frontpwd)




