from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addproducts(Form):
    name = StringField('Tên Sản Phẩm', [validators.DataRequired()])
    price = FloatField('Giá', [validators.DataRequired()])
    discount = IntegerField('Giảm Giá', default=0)
    stock = IntegerField('Tồn Kho', [validators.DataRequired()])
    colors = StringField('Màu Sắc', [validators.DataRequired()])
    discription = TextAreaField('Mô Tả', [validators.DataRequired()])

    image_1 = FileField('Hình 1')
    image_2 = FileField('Hình 2')
    image_3 = FileField('Hình 3')
