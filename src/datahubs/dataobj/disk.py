"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

from ujson import dump,load
from threading import Lock
import os
class Disk:
    def __init__(self, gid: int):
        self.gid = gid
        self.lock = Lock()
        self.filename = f'disk_{gid}.userspace.json'
        self.filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.join(__file__))),"storage",self.filename)
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
            with open(self.filepath, 'w+') as f:
                dump(self.data, f)
    def delete(self, key: str):
        with self.lock:
            try:
                del self.data[key]
                with open(self.filepath, 'w+') as f:
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