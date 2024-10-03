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

    def get(self, key: str) -> dict:
        raise Exception("need to override get")

    def update(self, key: str, data: dict):
        raise Exception("need to override update")
    
    
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
    
    def get(self, key: str) -> dict:
        try:
            return self._data[key]
        except:
            return dict()

    def update(self, key: str, data: dict):
        if key not in self._data:
            self._data.update({
                key: {}
            })
        self._data[key].update(data)


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
    
    def update(self, key: str, data: dict):
        super().hset(key, data)
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
    
    def get(self, key: str) -> dict:
        data = self._connection.hgetall(key)
        if data is None:
            return dict()
        
        return dict(map(lambda p: (p[0].decode(), p[1].decode()), data.items()))

    def update(self, key: str, data: dict):
        return self._connection.hset(key, mapping=data)
    

class MongoStorage(BaseStorage):
    def __init__(self, url: str = None, db_name: str = 'default', **kwargs) -> None:
        import pymongo
        if url is not None:
            client = pymongo.MongoClient(url)
        else:
            client = pymongo.MongoClient(**kwargs)

        self._db = client[db_name]

    def hget(self, key: str, hkey: str) -> Any:
        try:
            val = self._db[key].find_one({"key": hkey})
            assert val is not None
        except:
            raise VarDoesNotExistException

        val = val['value']
        if isinstance(val, bytes):
            return val.decode()
        
        return val
        
    def hset(self, key: str, hkey: str, value: Any):
        return self._db[key].replace_one({"key": hkey}, {"key": hkey, "value": value}, upsert=True)
    
    def get(self, key: str) -> dict:
        try:
            val = self._db[key]
            assert val is not None
        except:
            return dict()

        data = dict()
        for row in val.find():
            data[row['key']] = row['value']
        return data
    
    def update(self, key: str, data: dict):
        for hk, v in data.items():
            self.hset(key, hk, v)
    

class DjangoDBStorage(BaseStorage):
    def hget(self, key: str, hkey: str) -> Any:
        from varorm.dj.models import DBStorage
        row = DBStorage.objects.filter(key=key, hkey=hkey).first()
        if row is None:
            raise VarDoesNotExistException
        
        return row.value
    
    def hset(self, key: str, hkey: str, value: Any):
        from varorm.dj.models import DBStorage
        row = DBStorage.objects.filter(key=key, hkey=hkey).first() 
        if row is None:
            DBStorage(key=key, hkey=hkey, value=value).save()
        else:
            DBStorage.objects.filter(id=row.id).update(value=value)

    def get(self, key: str) -> dict:
        from varorm.dj.models import DBStorage
        data = dict()
        for row in DBStorage.objects.filter(key=key).all():
            data[row.hkey] = row.value
        return data

    def update(self, key: str, data: dict):
        for hk, v in data.items():
            self.hset(key, hk, v)
    