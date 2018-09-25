from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email,InputRequired,Length,EqualTo


class BaseForm(FlaskForm):
    @property
    def err(self):
        return self.errors.popitem()[1][0]

class UserForm(BaseForm):
    email=StringField(validators=[Email(message="必须为邮箱格式"),InputRequired(message='不能为空')])
    password=StringField(validators=[InputRequired(message='不能为空'),Length(min=6,max=40,message='长度在6-40位')])

class ResetPwdForm(BaseForm):
    oldpwd=StringField(validators=[InputRequired(message='必须输入旧密码')])
    newpwd=StringField(validators=[InputRequired(message='必须输入新密码')])
    newpwd2=StringField(validators=[EqualTo('newpwd',message='密码不一致')])


class ResetEmailSendCode(BaseForm):
    email = StringField(validators=[Email(message='必须为邮箱'), InputRequired(message='不能为空')])


class ResetEailForm(ResetEmailSendCode):
    emailCode=StringField(validators=[InputRequired(message='必须输入'),Length(min=6,max=6,message='验证码必须是6位')])

