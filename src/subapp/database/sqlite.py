from tortoise.models import Model
from tortoise import fields


class FileDB(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    path = fields.CharField(max_length=255)

    class Meta:
        table = "filedb"
        description = "file database"

