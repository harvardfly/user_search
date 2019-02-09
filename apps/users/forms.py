from wtforms_tornado import Form
from wtforms import StringField, DateField
from wtforms.validators import (
    DataRequired,
    Length
)


class RegisterForm(Form):
    username = StringField(
        validators=[
            DataRequired(message="请输入username"),
            Length(min=4, message='username长度不得小于4字节')
        ]
    )
    first_name = StringField(
        validators=[
            DataRequired(message="请输入first_name"),
            Length(max=20, message='first_name长度不得大于20字节')
        ]
    )
    last_name = StringField()
    address = StringField()
    description = StringField()
    birthday = DateField()
