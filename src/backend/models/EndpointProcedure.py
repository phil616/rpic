from .Basic import TimestampMixin
from tortoise import fields




class EndpointProcedure(TimestampMixin):
    endpoint_id = fields.IntField(pk=True,description="Endpoint ID, primary key")
    param_number = fields.IntField(description="Param Number")
    openapi_schema = fields.JSONField(description="OpenAPI Schema")
    namespace = fields.CharField(max_length=255,description="Namespace")
    mount_path = fields.CharField(max_length=255,description="Mount Path")
    class Meta:
        table = "endpoint_procedure"
        table_description = "Endpoint Procedure"