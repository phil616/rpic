from typing import Any

class PriorityList(list):
    def __init__(self,maxlen:int):
        super().__init__()
        self.maxlen = maxlen
        self._ddl = []

    def add(self, element:Any):
        if len(self._ddl) >= self.maxlen:
            self._ddl.pop(0)
        self._ddl.append(element)

    def remove(self,idx:int):
        self._ddl.pop(idx)

    def swap(self,idx1:int,idx2:int):
        self._ddl[idx1],self._ddl[idx2] = self._ddl[idx2],self._ddl[idx1]

    def __getitem__(self, idx:int):
        return self._ddl[idx]
    
