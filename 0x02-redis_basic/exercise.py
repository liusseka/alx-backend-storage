#!/usr/bin/env python
'''
Creates a cache class and store method
'''
import redis
import uuid
from functools import wraps


class Cache:
    '''Cache class for interacting with redis'''

    def __init__(self):
        '''Initialize redis client'''
        self._redis = redis.Redis()
        self.redis._redis.flushdb()

    def count_calls(method):
        """Decorator to count calls to a method."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data):
        '''Stores data in redis and returns key'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        """Retrieve data from Redis and
        convert it if a function is provided.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key):
        """Get string value from Redis."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """Get integer value from Redis."""
        return self.get(key, int)

    def call_history(method):
        """Decorator to track input and output history."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, output)
            return output
        return wrapper

    def replay(self, method):
        """Display the history of calls for a particular function."""
        inputs = self._redis.lrange(f"{method.__qualname__}:inputs", 0, -1)
        outputs = self._redis.lrange(f"{method.__qualname__}:outputs", 0, -1)
        count = len(inputs)
        print(f"{method.__qualname__} was called {count} times:")
        for inp, out in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{eval(inp.decode('utf-8'))})\
                  -> {out.decode('utf-8')}")
