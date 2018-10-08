#第三方的初始化

#对数据库各种操作
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

#对发送邮件各种操作
from flask_mail import Mail
mail=Mail()