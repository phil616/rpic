"""
鉴权核心模块
"""
from datetime import timedelta, datetime
from typing import Annotated, Dict
import jwt
from fastapi.security import  SecurityScopes
from fastapi import Request
from fastapi import Depends
from pydantic import ValidationError
from core.runtime import get_global_state
from conf import config
from core.exceptions import HTTP_E401
from core.security import CookieSecurity
from curd.authentication import user_scopes
from fastapi.security import OAuth2PasswordRequestForm
from core.logcontroller import log
from typing import Union

from fastapi.param_functions import Form

token_url = "/authorization/token"

oauth2_depends = CookieSecurity("/authorization/token", scopes=user_scopes)

def create_access_token(data: Dict) -> str:
    """
    构造JWT的token字符串函数
    将传进来的字典作为负载，并增加额外的默认字段后生成JWT的token字符串
    :param data: 负载数据
    :return: 负载数据被转换后的字符串
    """
    """
    额外注释：
    需要注意的是在RFC7519标准: https://www.rfc-editor.org/rfc/rfc7519    第四章中，标准负载包含了：
    "iss" (Issuer), 颁布者  本系统，颁布者为 APP_NAME
    "sub" (Subject),  主题  
    "aud" (Audience),  观众
    "exp" (Expiration Time), 过期时间
    "nbf" (Not Before), 生效时间
    "iat" (Issued At), 颁布时间
    "jti" (JWT ID) JWT ID
    Private Claim Names 私有声明
    1. "uid" (User) 用户ID
    2. "per" (Permission) 要求的权限
    使用的字段：
    1. "exp" (Expiration Time), 过期时间
    2. "uid" (User) 用户ID
    3. "per" (Permission) 要求的权限（根据权限颁发给用户的）  这和旧版系统的scopes字段相同，但不使用scopes字段
    4. "gid" (Group) 用户组ID
    5. "typ" (Type) 用户类型
    """
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_EXPIRE_MINUTES)  # JWT过期分钟 = 当前时间 + 过期时间
    token_data.update(
        {
            "exp": expire, 
            "iss": config.APP_NAME,
        }
    )
    jwt_token = jwt.encode(
        payload=token_data,             # 编码负载
        key=config.JWT_SECRET_KEY,      # 密钥
        algorithm=config.JWT_ALGORITHM  # 默认算法
    )
    log.debug(f"JWT_data: \n{token_data}\nJWT token: {jwt_token}")
    return jwt_token

def scope_contains(access_required_scope:list, user_has_scope:list) -> bool:
    """
    检查权限是否包含
    用于检查用户的权限是否包含所需的权限
    :param access_required_scope: 需要的权限
    :param user_has_scope: 用户的权限
    :return: 是否包含
    """
    return set(access_required_scope).issubset(set(user_has_scope))


async def check_permissions(
        req: Request,
        required_scope: SecurityScopes, 
        token=Depends(oauth2_depends),
        state = Depends(get_global_state)) -> None:
    
    """
    检查权限
    检查权限一般和fastapi的security的Depends一起使用，用于检查用户的权限是否满足要求
    :param req: 请求
    :param required_scope: 需要的权限
    :param token: token JWT原始token
    :param state: 全局状态
    """
    payload = None
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
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
    log.debug(f"User access scope: {required_scope.scopes}")
    if scope_contains(required_scope.scopes, user_requested_scope) is False:
        HTTP_E401("Not enough scope for authorization", {"WWW-Authenticate": f"Bearer {token}"})
    state.user = payload

class OAuth2WithGroupRequest(OAuth2PasswordRequestForm):
    """
    OAuth2带有用户组的模式类
    这个类与OAuth2PasswordRequestForm类相似，但是增加了用户组的字段，原始认证流程不变，但如果用户选择了用户组，那么用户组字段会被填充

    """

    def __init__(
        self,

        username: Annotated[
            str,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
        grant_type: Annotated[
            Union[str, None],
            Form(pattern="password"),
        ] = None,
        scope: Annotated[
            str,
            Form(),
        ] = "",
        client_id: Annotated[
            Union[str, None],
            Form(),
        ] = None,
        client_secret: Annotated[
            Union[str, None],
            Form(),
        ] = None,
        group_name: Annotated[
            Union[str, None],
            Form(),
        ] = None,
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.group_name = group_name
