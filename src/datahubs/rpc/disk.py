from ujson import dump,load
from threading import Lock
import os
class Disk:
    def __init__(self, gid: int):
        self.gid = gid
        self.lock = Lock()
        self.filename = f'disk_{gid}.json'
        self.filepath = os.path.join(__file__,"..","storage",self.filename)
        with self.lock:
            try:
                with open(self.filepath, 'r') as f:
                    self.data = load(f)
            except FileNotFoundError:
                self.data = {}
    def get(self, key: str):
        with self.lock:
            return self.data.get(key)
    def set(self, key: str, value):
        with self.lock:
            self.data[key] = value
            with open(self.filepath, 'w') as f:
                dump(self.data, f)
    def delete(self, key: str):
        with self.lock:
            try:
                del self.data[key]
                with open(self.filepath, 'w') as f:
                    dump(self.data, f)
            except KeyError:
                pass
    def update(self, key: str, value):
        with self.lock:
            self.data[key] = value
            with open(self.filepath, 'w') as f:
                dump(self.data, f)

class DiskPool:
    def __init__(self):
        self.disk_pool = {}
    
    def add_disk(self, disk: Disk):
        self.disk_pool[disk.gid] = disk

    def get_disk(self, gid: int):
        disk = self.disk_pool.get(gid)
        if not disk:
            disk = Disk(gid)
            self.add_disk(disk)
        return disk