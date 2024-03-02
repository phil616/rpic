from .Basic import TimestampMixin
from tortoise import fields


class Subapp(TimestampMixin):
    subapp_id = fields.IntField(pk=True,description="subapp id")
    subapp_host = fields.CharField(max_length=255,description="subapp host")
    subapp_port = fields.IntField(default=8000,description="subapp port")
    subapp_status = fields.BooleanField(default=True,description="status 0:not onlone 1:online")
    subapp_latest_report = fields.DatetimeField(description="last report time")

    class Meta:
        table = "subapp"
        table_description = "subapp info"
