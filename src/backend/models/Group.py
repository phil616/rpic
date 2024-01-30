from .Basic import TimestampMixin
from tortoise import fields
from tortoise.indexes import Index
class Group(TimestampMixin):
    group_id = fields.IntField(pk=True, description="Group ID, primary key")
    group_administrator = fields.ForeignKeyField("models.User", related_name="group_administrator", description="Group Administrator")
    group_name = fields.CharField(max_length=255, description="Group Name")
    group_info = fields.JSONField(description="Group Info")
    group_status = fields.IntField(description="Group Status")
    class Meta:
        table = "group"
        table_description = "Group Table"
        unique_together = (("group_id", "group_name"),)
        ordering = ["group_id"]
        indexes = [
            Index(
                fields=["group_id"],
                name="group_id_index"),
            Index(
                fields=["group_name"],
                name="group_name_index")
        ]
