import weakref
import functools
from collections import OrderedDict


class Cache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def __contains__(self, item):
        return item in self.cache

    def __getitem__(self, key):
        if key not in self.cache:
            return

        value = self.cache[key]
        self.cache.move_to_end(key)

        return value

    def __setitem__(self, key, value):
        if key in self.cache:
            del self.cache[key]

        weak_key = weakref.proxy(key)
        weak_value = weakref.proxy(value)
        self.cache[weak_key] = weak_value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class CacheWrapper:
    def __init__(self, capacity: int):
        self.__cache = Cache(capacity)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = (self.__freeze(args), self.__freeze(kwargs))
            if cache_key in self.__cache:
                return self.__cache[cache_key]

            function_work_result = func(*args, **kwargs)
            self.__cache[cache_key] = function_work_result
            return function_work_result

        return wrapped

    def __freeze(self, obj):
        if isinstance(obj, dict):
            return frozenset((key, self.__freeze(value)) for key, value in obj.items())
        elif isinstance(obj, list):
            return tuple(self.__freeze(value) for value in obj)
        elif isinstance(obj, set):
            return tuple(obj)
        return obj
