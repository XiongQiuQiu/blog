# -*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, \
    SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('你叫什么?', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('姓名',  validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名必须填写'
                                          '字母'
                                          '数字，点或下划线')
    ])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用')

class PostForm(Form):
    title = StringField('标题', validators=[DataRequired()])
    body = PageDownField('说说你的想法', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(Form):
    body = StringField('评论', validators=[DataRequired()])
    submit = SubmitField('提交评论')