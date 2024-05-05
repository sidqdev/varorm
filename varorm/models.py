import inspect

from typing import Any
from varorm.storage import BaseStorage
from varorm.fields import Field
from varorm.exceptions import VarDoesNotExistException


class Model:
    class Meta:
        key = None

    def __new__(cls):
        assert cls._storage is not None

        cls._fields = {}
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Field):
                cls._fields.update({
                    name: field
                })

        return super().__new__(cls)
    
    def _get_model_key(self) -> str:
        return self.Meta.key or self.__class__.__name__
    
    def _parse_field_data(self, __name, __value):
        return self._fields[__name].parse(__value)
    
    def _represent_field_data(self, __name, __value):
        value = self._fields[__name].parse(__value)
        return self._fields[__name].represent(value)
    
    def _get_from_storage(self, __name):
        return self._parse_field_data(__name, self._storage.hget(self._get_model_key(), __name))
    
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
    
    @classmethod
    def connect(cls, storage: BaseStorage):
        cls._storage = storage

 
