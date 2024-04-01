"""
运行时模块
"""


class SharedMemory(dict):
    """
    这个类是一个运行时共享的库
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SharedMemory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self["JWT_KEY"] = None
        self["JWT_ALGORITHM"] = None
        self["sp"] = None
        ...
    def get(self,key:str):
        return self[key]
        
    def set(self,key:str,value):
        self[key] = value


class GlobalState:
    def __init__(self):
        self.runtime = SharedMemory()
        """runtime fields:
        1. JWT_KEY JWT 密钥
        2. JWT_DECRYPT JWT解密算法
        3. DEPLOY_HOST 部署IP
        4. DEPLOY_PORT 部署端口
        5. GROUP_ID 组ID  # SP Specificated
        """
        ...

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)


G_state = GlobalState()


def get_global_state() -> GlobalState:
    return G_state
