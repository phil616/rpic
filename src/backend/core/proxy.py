from contextvars import ContextVar
from fastapi import Request

def bind_contextvar(contextvar):
    class ContextVarBind:
        __slots__ = ()

        def __getattr__(self, name):
            return getattr(contextvar.get(), name)

        def __setattr__(self, name, value):
            setattr(contextvar.get(), name, value)

        def __delattr__(self, name):
            delattr(contextvar.get(), name)

        def __getitem__(self, index):
            return contextvar.get()[index]

        def __setitem__(self, index, value):
            contextvar.get()[index] = value

        def __delitem__(self, index):
            del contextvar.get()[index]

    return ContextVarBind()


request_var: ContextVar[Request] = ContextVar("request")
request:Request = bind_contextvar(request_var)
"""request.userinfo = payload 
    1. "exp" (Expiration Time), 过期时间
    2. "uid" (User) 用户ID
    3. "per" (Permission) 要求的权限（根据权限颁发给用户的）  这和旧版系统的scopes字段相同，但不使用scopes字段
    4. "gid" (Group) 用户组ID
    5. "typ" (Type) 用户类型
"""