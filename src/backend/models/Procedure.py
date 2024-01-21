from .Basic import TimestampMixin

from tortoise import fields


class Procedure(TimestampMixin):
    procedure_id = fields.IntField(pk=True)