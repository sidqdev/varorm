from typing import Callable, Any
from datetime import date, datetime
from varorm import widgets
from varorm import exceptions


class Field:
    def __init__(
            self,
            base_type: Callable,
            verbose_name: str = None,
            choices: tuple = None,
            default: Any = None,
            null: bool = False,
        ) -> None:
        self._base_type = base_type
        self._verbose_name = verbose_name
        self._choices = choices
        self._default = default
        self._null = null

    def parse(self, value):
        if isinstance(value, str) and value == '':
            return None
        return self._base_type(value)
    
    def represent(self, value):
        return value
    
class IntegerField(Field):
    widget = widgets.IntegerWidget
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(int, *args, **kwargs)


class FloatField(Field):
    widget = widgets.FloatWidget
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(float, *args, **kwargs)


class BooleanField(Field):
    widget = widgets.BooleanWidget
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bool, *args, **kwargs)

    def parse(self, value) -> bool:
        if isinstance(value, str) and value == '':
            return None
        return bool(int(value))

    def represent(self, value: bool):
        return int(value)


class CharField(Field):
    widget = widgets.CharWidget
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(str, *args, **kwargs)


class TextField(Field):
    widget = widgets.TextWidget

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(str, *args, **kwargs)


class DateField(Field):
    widget = widgets.DateWidget

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(date, *args, **kwargs)

    def parse(self, value) -> date:
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except:
            pass
        try:
            return date.fromordinal(int(value))
        except:
            pass
        
        try:
            return date.fromtimestamp(float(value))
        except:
            pass
        
        raise exceptions.UnsupportableDateFormatException
    
    def represent(self, value):
        return date.isoformat(value)
    

class DateTimeField(Field):
    widget = widgets.DateTimeWidget
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(datetime, *args, **kwargs)

    def parse(self, value) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except:
            pass
        try:
            return datetime.fromordinal(int(value))
        except:
            pass
        try:
            return datetime.fromtimestamp(float(value))
        except:
            pass
        
        raise exceptions.UnsupportableDateTimeFormatException
    
    def represent(self, value):
        return datetime.isoformat(value)
