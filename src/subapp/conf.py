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
    AUTHCODE:str = Field(default="hello",env="AUTHCODE",description="向注册中心的认证码")
    
    SUBAPP_NAME:str = Field(default="CP",env="SUBAPP_NAME",description="SUBAPP的分类名字，CP或SP")
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
config = Config() # Singleton mode for config object
