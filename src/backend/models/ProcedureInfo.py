from .Basic import TimestampMixin

from tortoise import fields


class ProcedureInfo(TimestampMixin):
    procedure_id = fields.IntField(description="Procedure ID")
    procedure_name = fields.CharField(max_length=255,description="Procedure Name")
    procedure_decrypt_key = fields.CharField(max_length=255,description="Procedure Decrypt Key")
    procedure_encrypt_type = fields.CharField(default="AES",max_length=255,description="Procedure Encrypt Type AES/SM4")
    procedure_size = fields.IntField(description="Procedure Size")
    procedure_extra = fields.CharField(max_length=255,description="Procedure Info")
    class Meta:
        table = "procedure_info"
        table_description = "Procedure Info"


