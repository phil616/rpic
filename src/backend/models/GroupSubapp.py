from .Basic import TimestampMixin
from tortoise import fields


class GroupSubapp(TimestampMixin):
    group_id = fields.ForeignKeyField("models.Group", related_name="group_user", description="Group ID")
    subapp_id = fields.IntField(description="subapp_id,assigned by cp")
    class Meta:
        table = "group_subapp"
        table_description = "Group Subapp"
