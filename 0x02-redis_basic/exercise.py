#!/usr/bin/env python3
"""Module that creates Cache class."""
import redis
import uuid
import asyncio
from functools import wraps
from typing import Union, Callable, Any, Optional


def count_calls(method: Callable) -> Callable:
    """
        A decorator that count how many times
        methods of the Cache class are called
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output"""
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable):
    '''display the history of calls of a particular function.'''
    method = method.__qualname__
    client = redis.Redis()
    input_key = f"{method}:inputs"
    output_key = f"{method}:outputs"
    input_data = client.lrange(input_key, 0, -1)
    output_data = client.lrange(output_key, 0, -1)

    calls = len(input_data)
    print("{} was called {} times".format(method, calls))

    for inputs, outputs in zip(input_data, output_data):
        print("{}(*{}) -> {}".format(
            method, inputs.decode("utf-8"),
            outputs.decode("utf-8"))
            )


class Cache:
    def __init__(self) -> None:
        """Sets Up a connection to Redis"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the ke"""
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Gets and value from Redis data storage assiociated with key"""
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage"""
        return self.get(key, lambda v: v.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage"""
        return self.get(key, lambda v: int(v))
