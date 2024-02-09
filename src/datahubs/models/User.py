from tortoise.models import Model
from tortoise import fields

class User(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)