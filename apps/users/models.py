from peewee import *
from user_search.models import BaseModel


class User(BaseModel):
    username = CharField(max_length=50)
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=20, null=True)
    address = CharField(max_length=200, null=True)
    description = TextField(null=True)
    birthday = DateField(null=True)
