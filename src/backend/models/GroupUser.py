from .Basic import TimestampMixin
from tortoise import fields


class GroupUser(TimestampMixin):
    group_id = fields.IntField(description="Group ID")
    user_id = fields.IntField(description="Group User")
    class Meta:
        table = "group_user"
        table_description = "Group User"
