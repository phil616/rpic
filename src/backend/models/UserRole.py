from .Basic import TimestampMixin
from tortoise import fields



class UserRole(TimestampMixin):
    """
    User Role
    """
    user_id = fields.ForeignKeyField("models.User", related_name="user_role", description="User ID")
    user_roles = fields.CharField(max_length=255, description="User Roles")
    class Meta:
        table = "user_role"
        table_description = "User Role"
