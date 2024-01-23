from interface import Memory
from interface import FileStorage
from utils import generate_uuid

class GlobalDependency:
    def __init__(self):
        self.memories = {}
        self.diskes = {}
    def new_memory(self):
        m = Memory()
        mid = generate_uuid()
        self.memories.update({mid:m})
        return mid
    def new_disk(self):
        did = generate_uuid()
        d = FileStorage(str(did))
        self.diskes.update({did:d})
        return did
    def get_memory(self,mid):
        return self.memories.get(mid)
    def get_disk(self,did):
        return self.diskes.get(did)
    def get(self,mid):
        if mid in self.memories:
            return self.memories[mid]
        elif mid in self.diskes:
            return self.diskes[mid]
        else:
            return None
        

G_state = GlobalDependency()

def get_state():
    return G_state
