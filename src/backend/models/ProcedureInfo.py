"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

from .Basic import TimestampMixin

from tortoise import fields


class ProcedureInfo(TimestampMixin):
    procedure_id = fields.IntField(description="Procedure ID")
    procedure_name = fields.CharField(max_length=255,description="Procedure Name")
    procedure_decrypt_key = fields.CharField(max_length=255,description="Procedure Decrypt Key")
    procedure_encrypt_type = fields.CharField(default="AES",max_length=255,description="Procedure Encrypt Type AES/SM4")
    procedure_size = fields.IntField(null=True,description="Procedure Size")
    procedure_extra = fields.CharField(null=True,max_length=255,description="Procedure Info")
    class Meta:
        table = "procedure_info"
        table_description = "Procedure Info"


