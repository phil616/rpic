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

from .Basic import TimestampMixin
from tortoise import fields
from tortoise.indexes import Index



class User(TimestampMixin):
    """
    User Table
    """
    user_id = fields.IntField(pk=True, description="User ID, primary key")
    username = fields.CharField(max_length=255, unique=True, description="Username")
    password = fields.CharField(max_length=255, description="Password")
    user_info = fields.JSONField(description="User Info")
    user_status = fields.IntField(description="User Status")
    user_roles = fields.CharField(max_length=255, description="User Roles")
    class Meta:
        table = "user"
        table_description = "User Table"
        unique_together = (("user_id", "username"),)
        ordering = ["user_id"]
        indexes = [
            Index(
                fields=["user_id"],
                name="user_id_index"),
            Index(
                fields=["username"],
                name="username_index")
        ]
    
"""

[PROCEDURE:ACCESS]
1. GET  # 获取过程信息
2. EXCUTE  # 执行过程

[PROCEDURE:MODIFY]
1. CREATE  # 创建过程
2. UPDATE  # 更新过程
3. DELETE  # 删除过程
4. MOUNT   # 挂载过程
5. UNMOUNT # 卸载过程

[PROCEDURE:ADMIN]
1. ALTID  # 修改过程ID

[GROUP:CURD]
1. GET    # 获取组信息
2. DELETE # 删除组
3. UPDATE # 更新组
4. CREATE # 创建组

[GROUP:ENDPOINT]
1. ASSIGN  # 分配端点
2. RENAME  # 重命名端点
3. DELETE(DISABLE)  # 删除端点

[USER:CURD]
1. GET    # 获取用户信息
2. DELETE # 删除用户
3. UPDATE # 更新用户
4. CREATE # 创建用户

"""