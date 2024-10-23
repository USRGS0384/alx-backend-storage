#!/usr/bin/env python3
""" exercise.py """

from typing import Union, Optional, Callable
from functools import wraps
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """Increments the count for that key every time the method is
    called and returns the value returned by the original method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for
    a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs = str(args)
        self._redis.rpush(method.__qualname__ + ':inputs', inputs)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ':outputs', output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f"{key} was called {len(inputs)} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """Cache class."""

    def __init__(self):
        """Creates a connection with the db and clears cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates keys and stores data in the db."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float, None]:
        """Takes a key string argument and an optional Callable
        argument named fn. This callable will be used to convert
        the data back to the desired format.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Automatically parametrize Cache.get with the correct
        conversion function.
        """
        return self._redis.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        """Automatically parametrize Cache.get with the correct
          conversion function.
        """
        return int(self._redis.get(key).decode('utf-8'))
