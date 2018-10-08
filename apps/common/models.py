from exts import db
from datetime import datetime
import shortuuid
class Banner(db.Model):
    __tablename__='banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bannerName = db.Column(db.String(20), nullable=False)
    imglink = db.Column(db.String(200), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False, unique=True)
    priority = db.Column(db.Integer, default=1)


class Bank(db.Model):
    __tablename__ = 'bank'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bankname = db.Column(db.String(20),nullable=False)
    postnum = db.Column(db.String(200),nullable=False,default=0)
    create_time =db.Column(db.DateTime,default=datetime.now)

class Post(db.Model) :
    __tablename__ = "common_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    bank = db.relationship('Bank', backref='posts') #关联bank表
    # 前台用户id使用的short_uuid, 类型和长度，约束必须一直
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = db.relationship('FrontUser', backref='posts') # orm查询的时候使用
    readCount=db.Column(db.Integer,default=0) #浏览量

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey('common_post.id'))
    post=db.relationship('Post',backref=db.backref('tag',uselist=False))
    status = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Common(db.Model):
    __tablename__ = "common_common"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('common_post.id'))
    post = db.relationship('Post',backref='commons')
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = db.relationship('FrontUser', backref='commons')  # orm查询的时候使用
    create_time = db.Column(db.DateTime, default=datetime.now)
