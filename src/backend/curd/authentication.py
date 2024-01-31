from models.User import User
#from models.UserRole import UserRole  # User - Role
from models.RoleScope import RoleScope  # Role - Scope
from models.Group import Group
from models.GroupUser import GroupUser

user_scopes = {
    "PROCEDURE:ACCESS": "Access procedure",
    "PROCEDURE:MODIFY" : "Modify procedure",
    "PROCEDURE:ADMIN" : "manage procedure",
    "GROUP:CURD": "CURD group",
    "GROUP:ENDPOINT":"manage group endpoint",
    "USER:CURD":"CURD user"
}
user_roles = {
    "user": "application user",
    "creator": "procedure creator",
    "admin": "administrator of system",
    "system": "system admin"
}

async def curd_init_role_scope():
    """
    init role to scope mapping according to the doc:
    鉴权继承图 资源和用户设计
    """
    await RoleScope.create(
        user_role="user",
        role_scopes="PROCEDURE:ACCESS"
    )
    await RoleScope.create(
        user_role="creator",
        role_scopes="PROCEDURE:MODIFY"
    )
    await RoleScope.create(
        user_role="admin",
        role_scopes="PROCEDURE:ADMIN,GROUP:CURD,GROUP:ENDPOINT,USER:CURD"
    )
    await RoleScope.create(
        user_role="system",
        role_scopes="PROCEDURE:ACCESS,PROCEDURE:MODIFY,PROCEDURE:ADMIN,GROUP:CURD,GROUP:ENDPOINT,USER:CURD"
    )

async def get_user_permissions(user_id:int):
    """
    get user's permissions(scopes) by user id
    :param user_id: user id
    :return: List[str] permissions
    """
    ...

async def verify_user_password(username:str, password:str):
    """
    verify user's password
    :param username: username
    :param password: password
    :return: bool
    """
    user = await User.get(username=username)
    return user.password == password

async def curd_debug_test_user():
    user = await User.create(
        username="test1",
        password="test2",
        user_info={"test": "test"},
        user_roles="user",
        user_status=1,
    )
    print("debug user = ",user)


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
