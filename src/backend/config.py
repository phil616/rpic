from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
load_dotenv()

class AppConfig(BaseSettings):
    APP_NAME:str = Field(default="RPICS Backend", env="APP_NAME",description="APP名称")
    APP_VERSION:str = Field(default="0.0.1", env="APP_VERSION",description="APP版本")
    APP_TITLE:str = Field(default="RPICS", env="APP_TITLE",description="APP标题")
    APP_DESCRIPTION:str = Field(default="The backend for RPICS", env="APP_DESCRIPTION",description="APP描述")
    APP_DEBUG:bool = Field(default=False, env="APP_DEBUG",description="APP调试模式")



config = AppConfig()
