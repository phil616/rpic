from .Basic import TimestampMixin
from tortoise import fields


class GroupProcedure(TimestampMixin):
    group_id = fields.ForeignKeyField("models.Group", related_name="group_procedure", description="Group ID")
    procedure_id = fields.ForeignKeyField("models.Procedure", related_name="group_procedure", description="Group Procedure")
    class Meta:
        table = "group_procedure"
        table_description = "Group Procedure"
