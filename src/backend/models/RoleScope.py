
"""
    init role to scope mapping according to the doc:
    鉴权继承图 资源和用户设计
    
user: null = PROCEDURE:ACCESS
creator: user = PROCEDURE:MODIFY
admin: creator = PROCEDURE:ADMIN GROUP:CURD GROUP:ENDPOINT USER:CURD
system: admin = null

"""

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
