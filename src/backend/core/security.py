"""
安全处理模块
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
from urllib.parse import unquote

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from typing import Dict, Optional
from starlette.requests import Request
from typing import Any, Callable
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi.params import Depends
class CookieSecurity(OAuth2PasswordBearer):
    def __init__(self, tokenUrl:
                str,
                 scheme_name: Optional[str] = None,
                 scopes: Optional[Dict[str, str]] = None,
                 description: Optional[str] = None,
                 auto_error: bool = True,
                 cookie_name: str = "Authorization"
                 ) -> None:
        super().__init__(
            tokenUrl,
            scheme_name,
            scopes,
            description,
            auto_error,
        )
        self.cookie_name = cookie_name

    @staticmethod
    def partition_from_cookie(cookie_str: Optional[str]) -> str:
        if not cookie_str:
            return ""
        return unquote(cookie_str)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        cookie_authorization = request.cookies.get(self.cookie_name)  # get cookie auth string

        self.cookie_auth = self.partition_from_cookie(cookie_authorization)  # parse cookie string
        scheme, param = get_authorization_scheme_param(authorization)  # spilt header WWW-

        cookie_scheme, cookie_param = get_authorization_scheme_param(self.cookie_auth)  # spilt cookie string

        if cookie_param and cookie_scheme.lower() == "bearer":
            # Authorized by Cookie
            return cookie_param
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

class GroupSecurity(Depends):
    def __init__(
        self,
        dependency: Optional[Callable[..., Any]] = None,
        *,
        group: Optional[int] = None,
        use_cache: bool = True,
    ):
        super().__init__(dependency=dependency, use_cache=use_cache)
        self.group = group

def GroupPermission(dependency: 
        Optional[Callable[..., Any]] = None,
    *,
    group: 
        Optional[str]= None,
    use_cache:bool = True,):
    return GroupSecurity(dependency=dependency, group=group, use_cache=use_cache)