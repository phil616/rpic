from .Basic import TimestampMixin
from tortoise import fields


class GroupProcedure(TimestampMixin):
    group_id = fields.IntField(description="Group ID")
    procedure_id = fields.IntField(description="Group Procedure")
    class Meta:
        table = "group_procedure"
        table_description = "Group Procedure"
