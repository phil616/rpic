from Basic import TimestampMixin
from tortoise import fields

class User(TimestampMixin):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255,unique=True)
    password = fields.CharField(max_length=255)
    groups = fields.JSONField(default=[])
    role = fields.JSONField(default=[])
    is_active = fields.BooleanField(default=True)
    user_info = fields.JSONField(default={})
    user_email = fields.CharField(max_length=255,unique=True)
    user_phone = fields.CharField(max_length=255,unique=True)

    class Meta:
        table = "user"
        description = "user database"
    