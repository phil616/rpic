from .Basic import TimestampMixin
from tortoise import fields



class ProcedureExecute(TimestampMixin):
    procedure_id = fields.ForeignKeyField("models.Procedure",related_name="procedure_execute",description="Procedure ID")
    executed_by = fields.ForeignKeyField("models.User",related_name="procedure_execute",description="Executed By")
    executed_at = fields.DatetimeField(auto_now_add=True,description="Executed At")
    executed_from = fields.CharField(max_length=255,description="Executed From")

    class Meta:
        table = "procedure_execute"
        table_description = "Procedure Execute"