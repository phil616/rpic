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
