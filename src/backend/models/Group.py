from .Basic import TimestampMixin
from tortoise import fields

class Group(TimestampMixin):
    group_id = fields.IntField(pk=True,description="组ID，主键")
    group_name = fields.CharField(max_length=255,null=True,description="Group's name")
    group_admin = fields.CharField(max_length=255,description="who own this group")
    group_info = fields.JSONField(default={})

    class Meta:
        table = "group"
        description = "group database"

        