from .Basic import TimestampMixin
from tortoise import fields


class GroupUser(TimestampMixin):
    group_id = fields.ForeignKeyField("models.Group", related_name="group_user", description="Group ID")
    user_id = fields.ForeignKeyField("models.User", related_name="group_user", description="Group User")
    class Meta:
        table = "group_user"
        table_description = "Group User"
