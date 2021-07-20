from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError
from flask_wtf import FlaskForm, Form
from .models import User

#REGISTER
class RegistrationForm(FlaskForm):
    name = StringField('Họ và Tên', [validators.Length(min=4, max=25)])
    username = StringField('Tên Tài Khoản', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Mật Khẩu', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Nhập Lại Mật Khẩu')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Tên tài khoản đã tồn tại.')

        
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email đã tồn tại.')
            
#LOGIN
class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Mật Khẩu', [validators.DataRequired()])