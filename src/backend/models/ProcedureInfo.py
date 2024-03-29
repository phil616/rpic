from .Basic import TimestampMixin

from tortoise import fields


class ProcedureInfo(TimestampMixin):
    procedure_id = fields.IntField(description="Procedure ID")
    procedure_name = fields.CharField(max_length=255,description="Procedure Name")
    procedure_decrypt_key = fields.CharField(max_length=255,description="Procedure Decrypt Key")
    procedure_encrypt_type = fields.CharField(max_length=255,description="Procedure Encrypt Key")
    procedure_size = fields.IntField(description="Procedure Size")
    procedure_extra = fields.JSONField(description="Procedure Info")
    class Meta:
        table = "procedure_info"
        table_description = "Procedure Info"


