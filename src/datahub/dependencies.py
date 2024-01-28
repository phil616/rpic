from interface import Memory
from interface import FileStorage
from utils import generate_uuid
from typing import Dict

class GlobalDependency:
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self._disk_storage: Dict[str, FileStorage] = {}  
    # I don't know how this thing works, but it works
    @property
    def diskes(self) -> Dict[str, FileStorage]:
        class DiskStorage:
            def __init__(self, storage_dict: Dict[str, FileStorage]):
                self.storage_dict = storage_dict
                
            def __getitem__(self, key: str) -> FileStorage:
                if key in self.storage_dict:
                    return self.storage_dict[key]
                else:
                    loaded_file_storage = FileStorage(key)
                    self.storage_dict[key] = loaded_file_storage
                    return loaded_file_storage
        return DiskStorage(self._disk_storage)

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
        diskObj = self.diskes.get(did)
        if diskObj:
            return diskObj
        else:
            # load file from disk
            raise NotImplementedError
        
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
