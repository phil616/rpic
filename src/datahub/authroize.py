from datetime import timedelta, datetime
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,APIRouter
from pydantic import ValidationError,BaseModel
from fastapi import HTTPException
from passlib.hash import sha256_crypt
from utils import write_file,get_boot_time,verify_password,generate_password_hash
from control import User
from fastapi import Request

def E401(detail, headers):
    raise HTTPException(status_code=401, detail=detail, headers=headers)
authorize_router = APIRouter()
write_file("boot_time",get_boot_time().encode())
with open("boot_time", "r") as f:
    boot_time = f.read()

JWT_SECRET_KEY = sha256_crypt.hash(boot_time)

def create_access_token(data: dict) -> str:
    """
    返回JWT的token字符串
    :param data: 负载数据
    :return: 负载数据被转换后的字符串
    """
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)  # JWT过期分钟 = 当前时间 + 过期时间
    token_data.update(
        {
            "exp": expire,  # 根据RFC7519标准， https://www.rfc-editor.org/rfc/rfc7519，该字段为判断过期时间的字段
        }
    )
    jwt_token = jwt.encode(payload=token_data,  # 编码负载
                           key=JWT_SECRET_KEY,  # 密钥
                           algorithm='HS256')  # 默认算法
    return jwt_token


OAuth2 = OAuth2PasswordBearer("/authorization/token")


async def check_permissions(req:Request,token=Depends(OAuth2)) -> None:
    payload = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        if not payload:
            E401("Invalid certification", {"WWW-Authenticate": f"Bearer {token}"})
        req.app.state.username = payload.get("username")
    except jwt.ExpiredSignatureError:
        E401("Certification has expired", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.InvalidTokenError:
        E401("Certification parse error", {"WWW-Authenticate": f"Bearer {token}"})
    except (jwt.PyJWTError, ValidationError):
        E401("Certification parse failed", {"WWW-Authenticate": f"Bearer {token}"})

class UserVerifySchema(BaseModel):
    username: str
    password: str

@authorize_router.post("/token")
async def authorize_router_get_token(model:UserVerifySchema):
    user = await User.filter(username=model.username).first()
    if user is None:
        E401("Invalid username", {"WWW-Authenticate": "Bearer"})
    if not verify_password(model.password,user.password):
        E401("Invalid password", {"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token({"username": model.username})}

class UserRegisterSchema(BaseModel):
    username: str
    id: int

@authorize_router.post("/register")
async def authorize_router_register(model:UserVerifySchema,key:str):
    if key != "datahub":
        E401("Invalid key", {"WWW-Authenticate": "Bearer"})
    user = await User.create(
        username=model.username,
        password=generate_password_hash(model.password)
    )
    return UserRegisterSchema(**user.__dict__)