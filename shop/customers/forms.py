from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register




class CustomerRegisterForm(FlaskForm):
    name = StringField('Họ và Tên: ')
    username = StringField('Tên Tài Khoản: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Mật Khẩu: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Nhập Lại Mật Khẩu: ', [validators.DataRequired()])
    country = StringField('Quốc Gia: ', [validators.DataRequired()])
    city = StringField('Thành Phố: ', [validators.DataRequired()])
    contact = StringField('Liên Lạc: ', [validators.DataRequired()])
    address = StringField('Địa Chỉ: ', [validators.DataRequired()])
    zipcode = StringField('Zip code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Đăng Ký')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Tên tài khoản này đã được sử dụng!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Email này đã được sử dụng")

    


class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Mật Khẩu: ', [validators.DataRequired()])

   




   

 

    

     

   


    

