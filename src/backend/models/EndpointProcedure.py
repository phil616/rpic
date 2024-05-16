from .Basic import TimestampMixin
from tortoise import fields




class EndpointProcedure(TimestampMixin):
    endpoint_id = fields.IntField(pk=True,description="Endpoint ID, primary key")
    namespace = fields.CharField(max_length=255,description="Namespace")
    mount_path = fields.CharField(max_length=255,description="Mount Path")
    procedure_id = fields.IntField(null=False,description="Procedure ID")
    class Meta:
        table = "endpoint_procedure" 
        table_description = "Endpoint Procedure"