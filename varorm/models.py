import inspect
from typing import Any

from varorm.storage import BaseStorage
from varorm.fields import Field
from varorm.exceptions import *


class Model:
    class Meta:
        pass

    class _meta:
        key = None
        groups = None
        verbose_name = None
        init_load = False

    def __new__(cls, key=None):
        assert cls._storage is not None
        cls.key = key

        cls._fields = {}
        cls._preloaded_data = None

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Field):
                cls._fields.update({
                    name: field
                })
        
        return super().__new__(cls)

    def __init__(self, *args, **kwargs) -> None:
        if self.get_meta().init_load:
            self._load_data()
        
        super().__init__(*args, **kwargs)

    def _load_data(self):
        self._preloaded_data = self._storage.get(self._get_model_key())
            
    @classmethod
    def get_meta(cls):
        meta = cls._meta()

        for k, v in inspect.getmembers(cls.Meta):
            if not k.startswith("__"):
                setattr(meta, k, v)
        
        return meta
    
    def _get_model_key(self) -> str:
        return self.key or self.get_meta().key or self.__class__.__name__
    
    def _parse_field_data(self, __name, __value):
        return self._fields[__name].parse(__value)
    
    def _represent_field_data(self, __name, __value):
        value = self._fields[__name].parse(__value)
        return self._fields[__name].represent(value)
    
    def _get_from_storage(self, __name):
        if self._preloaded_data is None:
            value = self._storage.hget(self._get_model_key(), __name)
        else:
            try:
                value = self._preloaded_data[__name]
            except:
                raise VarDoesNotExistException

        return self._parse_field_data(__name, value)
    
    def _set_to_storage(self, __name, __value):
        self._storage.hset(self._get_model_key(), __name, self._represent_field_data(__name, __value))

    def __getattribute__(self, __name: str) -> Any:
        if __name == '_fields' or __name not in self._fields:
            return super().__getattribute__(__name)
        
        try:
            return self._get_from_storage(__name)
        except VarDoesNotExistException:
            field = self._fields[__name]
            if field._default is not None:
                return field._default
            elif field._null:
                return None
            raise VarDoesNotExistException

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name not in self._fields:
            return super().__setattr__(__name, __value)
        self._set_to_storage(__name, __value)
        if self.get_meta().init_load:
            self._load_data()
    
    def update(self, **data):
        validated_data = dict()
        for k, v in data.items():
            if k not in self._fields.keys():
                raise KeyNotFoundException(f"{k}")
            validated_data[k] = self._represent_field_data(k, v)
        self._storage.update(self._get_model_key(), validated_data)
        if self.get_meta().init_load:
            self._load_data()
            
    @classmethod
    def connect(cls, storage: BaseStorage):
        cls._storage = storage

 