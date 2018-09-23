from flask import Flask
from exts import db
import config
from apps.cms.urls import bp as cms_bp
from apps.front.urls import bp as front_bp
from flask_wtf import CSRFProtect


app=Flask(__name__)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)


#告诉主程序要映射数据库了
app.config.from_object(config)
CSRFProtect(app=app)

db.init_app(app=app)





if __name__ == '__main__':
    app.run()
