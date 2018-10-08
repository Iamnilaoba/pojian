from ce import celery_server,app
from exts import mail
from flask_mail import Message
from dysms_python.demo_sms_send import send_sms

@celery_server.task
def sendmsg(recvmail,r):
    with app.app_context():
        msg = Message("破茧科技更新邮箱验证码", recipients=[recvmail], body="验证码为" + r)
        mail.send(msg)

@celery_server.task
def sendcmscode(phone,code):
    send_sms(phone_numbers=phone,smscode=code)
