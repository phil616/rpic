from pydantic_settings import BaseSettings
from pydantic import Field

class Config(BaseSettings):

    # Basic info for app's OpenAPI schema
    APP_NAME:str = Field(default="RPICS Backend", env="APP_NAME",description="APP名称")
    APP_VERSION:str = Field(default="0.0.1", env="APP_VERSION",description="APP版本")
    APP_TITLE:str = Field(default="RPICS", env="APP_TITLE",description="APP标题")
    APP_DESCRIPTION:str = Field(default="The backend for RPICS", env="APP_DESCRIPTION",description="APP描述")
    APP_DEBUG:bool = Field(default=True, env="APP_DEBUG",description="APP调试模式")

    CP_HOST:str = Field(default="127.0.0.1",env="CP_HOST")

    DEPLOY_PORT:int = Field(default=8001,env="DEPLOY_PORT",description="部署端口")

config = Config() # Singleton mode for config object
