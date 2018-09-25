#第三方的初始化
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

from flask_mail import Mail
mail=Mail()