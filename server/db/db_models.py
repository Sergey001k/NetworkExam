from tortoise.models import Model
from tortoise import fields

class Admin(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=256, unique=True)
    username = fields.CharField(max_length=256)
    password = fields.CharField(max_length=256)

    class Meta:
        table = "admins"