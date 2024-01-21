from Basic import TimestampMixin
from tortoise import fields

class Group(TimestampMixin):
    group_id = fields.IntField(pk=True)
    group_name = fields.CharField(max_length=255,unique=True)
    group_admin = fields.CharField(max_length=255)
    group_info = fields.JSONField(default={})

    class Meta:
        table = "group"
        description = "group database"

        