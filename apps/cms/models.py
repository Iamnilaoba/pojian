from exts import db
from datetime import datetime

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(40),nullable=False)
    email=db.Column(db.String(30),nullable=False,unique=True)
    join_time=db.Column(db.DateTime,default=datetime.now)
