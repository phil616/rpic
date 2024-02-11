from dataobj.cache import CachePool
from dataobj.disk import DiskPool

g_cache = CachePool()  # g_ means global or singleton
g_disk = DiskPool()