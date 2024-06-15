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

