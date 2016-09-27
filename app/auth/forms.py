# -*- coding=utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('邮箱/email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我的登陆')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    email = StringField('邮箱/email', validators=[DataRequired(), Length(1, 64),
                                                Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp(ur'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', 0,
                                              '用户名只能包含中文'
                                              '字母'
                                              '数字或下划线')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[
        DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('更改密码')
class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validator=[DataRequired(), Length(1, 64),
                                         Email()])
    submit = SubmitField('重置密码')

class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('不存在的邮箱地址')

class ChangeEmailForm(Form):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('更新邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')