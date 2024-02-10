from fastapi import Request, Depends
from fastapi.security import SecurityScopes
from pydantic import ValidationError

import jwt
from fastapi.exceptions import HTTPException as HTTP_E401
from webcore.logcontroller import log
from webcore.dependenices import get_global_state


async def check_permissions(
        req: Request,
        required_scope: SecurityScopes, 
        state = Depends(get_global_state)) -> None:
    
    """
    检查权限
    检查权限一般和fastapi的security的Depends一起使用，用于检查用户的权限是否满足要求
    :param req: 请求
    :param required_scope: 需要的权限
    :param state: 全局状态
    """
    token = req.headers.get("Authorization").split(" ")[1]
    payload = None
    try:
        payload = jwt.decode(token, state.runtime.get("JWT_KEY"), algorithms=[state.runtime.get("JWT_KEY")])
        log.debug(f"Payload: {payload}")
        if not payload:
            HTTP_E401("Invalid certification", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.ExpiredSignatureError:
        HTTP_E401("Certification has expired", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.InvalidTokenError:
        HTTP_E401("Certification parse error", {"WWW-Authenticate": f"Bearer {token}"})
    except (jwt.PyJWTError, ValidationError):
        HTTP_E401("Certification parse failed", {"WWW-Authenticate": f"Bearer {token}"})
    user_requested_scope = payload.get("per")
    log.debug(f"User requested scope: {user_requested_scope}")
    if not set(user_requested_scope).issubset(set(required_scope.scopes)):
        HTTP_E401("Not enough scope for authorization", {"WWW-Authenticate": f"Bearer {token}"})
    state.user = payload
