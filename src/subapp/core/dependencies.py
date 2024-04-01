from core.syscache import SystemCache


class GlobalState:
    def __init__(self):
        self.runtime = SystemCache()
        """runtime fields:
        1. JWT_KEY JWT 密钥
        2. JWT_DECRYPT JWT解密算法
        3. DEPLOY_HOST 部署IP
        4. DEPLOY_PORT 部署端口
        5. GROUP_ID 组ID
        """

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)


G_state = GlobalState()

def get_global_state() -> GlobalState:
    return G_state
