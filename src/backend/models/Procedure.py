from .Basic import TimestampMixin

from tortoise import fields
from tortoise.indexes import Index

class Procedure(TimestampMixin):
    procedure_id = fields.IntField(pk=True,description="Procedure ID, primary key")
    procedure_type = fields.CharField(max_length=255,description="Script or Package")
    procedure_creator = fields.ForeignKeyField("models.User",related_name="procedure_creator",description="Procedure Creator")
    procedure_group_id = fields.ForeignKeyField("models.Group",related_name="procedure_group_id",description="Procedure Group ID")
    memory_id = fields.CharField(max_length=255,description="Memory ID")
    disk_id = fields.CharField(max_length=255,description="Disk ID")
    execute_type = fields.CharField(max_length=255,description="Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]")
    endpoint_id = fields.CharField(max_length=255,description="Endpoint ID")

    class Meta:
        table = "procedure"
        table_description = "Procedure Table"
        unique_together = (("procedure_id", "procedure_type"),)
        ordering = ["procedure_id"]
        indexes = [
            Index(
                fields=["procedure_id"],
                name="procedure_id_index"),
            Index(
                fields=["procedure_type"],
                name="procedure_type_index")
        ]

class ProcedureInfo(TimestampMixin):
    procedure_id = fields.ForeignKeyField("models.Procedure",related_name="procedure_info",description="Procedure ID")
    procedure_name = fields.CharField(max_length=255,description="Procedure Name")
    procedure_decrypt_key = fields.CharField(max_length=255,description="Procedure Decrypt Key")
    procedure_encrypt_type = fields.CharField(max_length=255,description="Procedure Encrypt Key")
    procedure_size = fields.IntField(description="Procedure Size")
    procedure_extra = fields.JSONField(description="Procedure Info")
    class Meta:
        table = "procedure_info"
        table_description = "Procedure Info"

class ProcedureExecute(TimestampMixin):
    procedure_id = fields.ForeignKeyField("models.Procedure",related_name="procedure_execute",description="Procedure ID")
    executed_by = fields.ForeignKeyField("models.User",related_name="procedure_execute",description="Executed By")
    executed_at = fields.DatetimeField(auto_now_add=True,description="Executed At")
    executed_from = fields.CharField(max_length=255,description="Executed From")

    class Meta:
        table = "procedure_execute"
        table_description = "Procedure Execute"

class EndpointProcedure(TimestampMixin):
    endpoint_id = fields.IntField(pk=True,description="Endpoint ID, primary key")
    param_number = fields.IntField(description="Param Number")
    openapi_schema = fields.JSONField(description="OpenAPI Schema")
    namespace = fields.CharField(max_length=255,description="Namespace")
    mount_path = fields.CharField(max_length=255,description="Mount Path")
    class Meta:
        table = "endpoint_procedure"
        table_description = "Endpoint Procedure"