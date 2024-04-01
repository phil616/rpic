from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from os import path,walk

def get_models() -> list:
    """
    获取model文件夹下的文件 即需要注册到MySQL的Model
    :return:
    """
    skip_files = ['Basic.py', '__init__.py']
    ret = []
    for _, _, i in walk(path.join("models")):
        models = list(set(i) - set(skip_files))
        for model in models:
            model = model.replace(".py", "")
            model = "models." + model
            ret.append(model)
        break

    return ret

load_dotenv()

class AppConfig(BaseSettings):

    # Basic info for app's OpenAPI schema
    APP_NAME:str = Field(default="RPICS Backend", env="APP_NAME",description="APP名称")
    APP_VERSION:str = Field(default="0.0.1", env="APP_VERSION",description="APP版本")
    APP_TITLE:str = Field(default="RPICS", env="APP_TITLE",description="APP标题")
    APP_DESCRIPTION:str = Field(default="The backend for RPICS", env="APP_DESCRIPTION",description="APP描述")
    APP_DEBUG:bool = Field(default=True, env="APP_DEBUG",description="APP调试模式")


    # -------------------- MYSQL --------------------
    # MySQL config for tortoise ORM
    MYSQL_HOST:str = Field(default="localhost", env="MYSQL_HOST",description="MySQL主机地址")
    MYSQL_PORT:int = Field(default=3306, env="MYSQL_PORT",description="MySQL端口")
    MYSQL_USER:str = Field(default="root", env="MYSQL_USER",description="MySQL用户名")
    MYSQL_PASS:str = Field(default="123456", env="MYSQL_PASS",description="MySQL密码")
    MYSQL_DB:str = Field(default="rpics", env="MYSQL_DB",description="MySQL数据库名称")
    GLOBAL_TIMEZONE: str = Field(default="Asia/Shanghai", env="GLOBAL_TIMEZONE",description="全局时区")

    # -------------------- JWT --------------------
    # JWT (Json Web Token) 
    JWT_SECRET_KEY: str = Field(default="randomkey",env="JWT_SECRET_KEY",description="JWT密钥")
    JWT_ACCESS_EXPIRE_MINUTES: int = Field(default=24*60,env="JWT_ACCESS_EXPIRE_MINUTES",description="JWT过期时间")
    JWT_ALGORITHM: str = Field(default="HS256",env="JWT_ALGORITHM",description="JWT算法")
    # -------------------- CORS --------------------
    # Cross-Origin Resource Sharing Policy
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # -------------------- RPC --------------------
    # RPC config
    RPC_ROOT_SERVER: str = Field(default="localhost", env="RPC_ROOT_SERVER",description="RPC根服务器地址")
    RPC_ROOT_PORT: int = Field(default=8000, env="RPC_ROOT_PORT",description="RPC根服务器端口")
    RPC_ROOT_USERNAME: str = Field(default="admin", env="RPC_ROOT_USERNAME",description="RPC根服务器用户名")
    RPC_ROOT_PASSWORD: str = Field(default="admin", env="RPC_ROOT_PASSWORD",description="RPC根服务器密码")
    # -------------------- SQLite --------------------
    # SQLite config for tortoise ORM
    SQLITE_DIR: List = [".","sqlite3"]
    SQLITE_FILE: str = "rpics.db"
    SQLITE_URL: str = path.join(*SQLITE_DIR,SQLITE_FILE)
    SQLITE_MODELS: list = get_models()
    
    DEPLOY_PORT:int = Field(default=9000,env="DEPLOY_PORT",description="部署端口")
    AUTHCODE:str = Field(default="hello",env="AUTHCODE",description="向注册中心的认证码")
    
    SUBAPP_NAME:str = Field(default="DB",env="SUBAPP_NAME",description="SUBAPP的分类名字，CP或SP")
    SUBAPP_AUTHCODE:str = Field(default="hello",env="SUBAPP_AUTHCODE",description="子应用的授权码")
    SUBAPP_EXPIRE:int = Field(default=300,env="SUBAPP_EXPIRE",description="最大过期时间")

    # -------------------- RabbitMQ --------------------
    MQ_URI:str = Field(default="amqp://guest:guest@localhost/",env="MQ_URI",description="RabbitMQ的URI")
    MQ_SHARE:str = Field(default="shared_applications",env='MQ_SHARE',description="共享队列的路由名称")

    # -------------------- Cache Json MQ ---------------
    REDIS_MQ_URI:str = Field(default="redis://localhost",env="REDIS_SERVER",description="RedisMQ服务器")
    REDIS_SERVER:str = Field(default="localhost",env="REDIS_SERVER",description="Redis服务器")

    # -------------------- ETCD Service ---------------
    ETCD_HOST:str = Field(default="localhost",env="ETCD_HOST",description="ETCD服务的部署地址")
    ETCD_PORT:int = Field(default=2379,env="ETCD_PORT",description="ETCD服务的部署端口，默认2379")

config = AppConfig()
