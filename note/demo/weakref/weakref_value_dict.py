import gc
import sys
import threading

import weakref


class Data:
    """数据缓存"""
    def __init__(self, key):
        pass


class Cache:
    """数据缓存"""
    def __init__(self):
        # WeakValueDictionary：当value没有引用时候，会自动删除对应的key和value
        self.pool = weakref.WeakValueDictionary()
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            data = self.pool.get(key)
            if data:
                print("from cache")
                return data

            print("create")
            data = Data(key)
            print(sys.getrefcount(data))

            # 这个只缓存了data 的弱引用（不做计数增加）
            self.pool[key] = data
            print(sys.getrefcount(data))
            return data


c = Cache()

# 第一次获取创建新的
d = c.get("hello")

# sys.getrefcount(d) 时候会增加计数， 返回后释放
print(sys.getrefcount(d))

print(d)
print(c.get("hello"))
print(c.get("hello") is d)
print(sys.getrefcount(d))

print("\nafter release:")
d = 123

# 修改d 或 del d 会做减计数， 而释放d, 再次获取的时候为None
print(c.get("hello"))
print(c.get("hello") is d)

