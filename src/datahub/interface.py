import os
import warnings
import ujson as json
import threading
class SharedObject:
    def __init__(self, *args, **kwargs):
        pass
    def delete(self):
        raise NotImplementedError
    def update(self):
        raise NotImplementedError
    def create(self):
        raise NotImplementedError
    def get(self):
        raise NotImplementedError

class Memory(SharedObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = {}
    def delete(self, key):
        del self._data[key]
    def update(self, key, value):   
        self._data[key] = value
    def create(self, key, value):
        self._data[key] = value
    def set(self, key, value):
        self._data[key] = value
    def get(self, key):
        # make sure there is no KeyError
        return self._data.get(key)
    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value
    def __delitem__(self, key):
        del self._data[key]
    def __contains__(self, key):
        return key in self._data
    

class FileStorage(SharedObject):
    
    def __init__(self, localdb: os.PathLike = None) -> None:
        self._cache = dict()
        self._mutex = threading.Lock()
        self._localdb = localdb
        if self._localdb is not None:
            with self._mutex:
                self._load()

    def _load(self):
        if os.path.exists(self._localdb):
            with open(self._localdb) as f:
                self._cache = json.load(f)
        else:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def set(self, key, value):
        if key in self._cache:
            warnings.warn('Key already exists, will be overwritten.')
        self._cache[key] = value

    def get(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
            return None
        return self._cache[key]

    def remove(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
        del self._cache[key]

    def clear(self):
        self._cache.clear()

    def submit(self):
        if self._localdb is None:
            warnings.warn('Local database not specified.')
            return
        # with lock
        with self._mutex:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
        self.submit()
