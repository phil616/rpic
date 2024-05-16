from .Basic import TimestampMixin

from tortoise import fields
from tortoise.indexes import Index

class Procedure(TimestampMixin):
    procedure_id = fields.IntField(pk=True,description="Procedure ID, primary key")
    procedure_type = fields.CharField(max_length=255,description="Script or Package")
    procedure_creator = fields.CharField(max_length=255,description="Procedure Creator")
    procedure_group_id = fields.IntField(description="Procedure Group ID")
    memory_id = fields.CharField(max_length=255,description="Memory ID")
    disk_id = fields.CharField(max_length=255,description="Disk ID")
    execute_type = fields.CharField(default="MOUNT AND EXECUTE",max_length=255,description="Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]")
    endpoint_id = fields.CharField(null=True,max_length=255,description="Endpoint ID")
    procedure_raw = fields.TextField(description="raw body")
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

