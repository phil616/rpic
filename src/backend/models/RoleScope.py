from .Basic import TimestampMixin
from tortoise import fields


class RoleScope(TimestampMixin):
    """
    Role Scope
    """
    user_role = fields.CharField(max_length=255, description="User Roles")
    role_scopes = fields.CharField(max_length=255, description="Role Scopes")
    class Meta:
        table = "role_scope"
        table_description = "Role Scope"
