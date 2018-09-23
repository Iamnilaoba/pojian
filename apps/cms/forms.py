from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email,InputRequired,Length


class BaseForm(FlaskForm):
    @property
    def err(self):
        return self.errors.popitem()[1][0]

class UserForm(BaseForm):
    email=StringField(validators=[Email(message="必须为邮箱格式"),InputRequired(message='不能为空')])
    password=StringField(validators=[InputRequired(message='不能为空'),Length(min=6,max=40,message='长度在6-40位')])

