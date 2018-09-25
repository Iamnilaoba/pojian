from flask import Flask
from exts import db,mail
import config
from apps.cms.urls import bp as cms_bp
from apps.front.urls import bp as front_bp
from flask_wtf import CSRFProtect
from flask_mail import Message

app=Flask(__name__)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)


#告诉主程序要映射数据库了
app.config.from_object(config)
CSRFProtect(app=app)

db.init_app(app=app)
mail.init_app(app)




if __name__ == '__main__':
    app.run()
