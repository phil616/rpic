from .Basic import TimestampMixin
from tortoise import fields


class GroupDatahub(TimestampMixin):
    group_id = fields.IntField(description="Group ID")
    datahub_id = fields.IntField(description="datahub_id,assigned by cp")
    class Meta:
        table = "group_datahub"
        table_description = "Group Datahub"
