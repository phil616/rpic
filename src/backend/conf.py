from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from os import path, walk
from typing import List
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
    APP_DEBUG:bool = Field(default=False, env="APP_DEBUG",description="APP调试模式")


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
    # -------------------- CORS --------------------
    # Cross-Origin Resource Sharing Policy
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    
config = AppConfig()
