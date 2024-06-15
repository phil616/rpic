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

# -*- coding:utf-8 -*-

from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    update_by = fields.CharField(max_length=255,null=True,default="[system]", description="更新人")
    create_by = fields.CharField(max_length=255,null=True,default="[system]", description="创建人")

    class Meta:
        abstract = True
