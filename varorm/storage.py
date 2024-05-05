import os
import json
import pickle
from typing import Any, Callable

from varorm.exceptions import VarDoesNotExistException

class BaseStorage:
    def hget(self, key: str, hkey: str) -> Any:
        raise Exception("need to override hget")
    
    def hset(self, key: str, hkey: str, value: Any):
        raise Exception("need to override hset")


class MemoryStorage(BaseStorage):
    def __init__(self) -> None:
        self._data = {}

    def hget(self, key: str, hkey: str) -> Any:
        try:
            return self._data[key][hkey]
        except:
            raise VarDoesNotExistException
    
    def hset(self, key: str, hkey: str, value: Any):
        if key not in self._data:
            self._data.update({
                key: {}
            })
        self._data[key].update({
            hkey: value
        })


class FileStorage(MemoryStorage):
    def __init__(
            self, 
            path: str, 
            load_function: Callable, # ex. json.load
            dump_function: Callable, # ex. json.dump
            is_binary_mode: bool = False, # For pickle = True
            save_on_set: bool = False
        ) -> None:
        super().__init__()

        self._path = path
        self._read_mode = 'rb' if is_binary_mode else 'r'
        self._write_mode = 'wb' if is_binary_mode else 'w'

        self._load_function = load_function
        self._dump_function = dump_function
        self._save_on_set = save_on_set


        if os.path.isfile(self._path):
            with open(self._path, self._read_mode) as f:
                self._data = self._load_function(f)
        
    def save(self):
        with open(self._path, self._write_mode) as f:
            self._dump_function(self._data, f)
    
    def hset(self, key: str, hkey: str, value: Any):
        super().hset(key, hkey, value)
        if self._save_on_set:
            self.save()


class JsonStorage(FileStorage):
    def __init__(self, path: str, save_on_set: bool = False) -> None:
        super().__init__(path, json.load, json.dump, False, save_on_set)


class PickleStorage(FileStorage):
    def __init__(self, path: str, save_on_set: bool = False) -> None:
        super().__init__(path, pickle.load, pickle.dump, True, save_on_set)


class RedisStorage(BaseStorage):
    def __init__(self, url: str = None, **kwargs) -> None:
        import redis
        if url is not None:
            connection = redis.Redis.from_url(url)
        else:
            connection = redis.Redis(**kwargs)

        connection.ping()
        self._connection = connection

    def hget(self, key: str, hkey: str) -> Any:
        if not self._connection.hexists(key, hkey):
            raise VarDoesNotExistException
        val = self._connection.hget(key, hkey)

        if isinstance(val, bytes):
            return val.decode()
        
        return val
        
    def hset(self, key: str, hkey: str, value: Any):
        return self._connection.hset(key, hkey, value)
    
