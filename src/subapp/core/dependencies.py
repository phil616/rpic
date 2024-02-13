from core.syscache import SystemCache


class GlobalState:
    def __init__(self):
        self.runtime = SystemCache()

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)


G_state = GlobalState()

def get_global_state() -> GlobalState:
    return G_state
