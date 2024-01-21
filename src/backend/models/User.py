from .Basic import TimestampMixin
from tortoise import fields

class User(TimestampMixin):
    """
    User Table, define the basic user of the system
    """
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255,unique=True,description="Username for login")
    password = fields.CharField(max_length=255,description="Password for login")
    groups = fields.JSONField(default=[],description="groups it have")
    role = fields.JSONField(default=[],description="role of this user, admin/user/system")
    is_active = fields.BooleanField(default=True,description="availiable")
    user_info = fields.JSONField(default={},description="user's extra info")
    user_email = fields.CharField(max_length=255,unique=True,null=True,description="user's email")
    user_phone = fields.CharField(max_length=255,unique=True,null=True,description="user's phone number")

    class Meta:
        table = "user"
        description = "user database"
