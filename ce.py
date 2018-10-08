from flask import Flask
from celery import Celery
from exts import mail
import config


app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)

celery_server = Celery(__name__,include=['tasks'])
celery_server.config_from_object(config)

if __name__ == '__main__':
    app.run()