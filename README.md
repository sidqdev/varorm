## varorm - variables orm with django admin support

#### v0.0.1 - Basic models and Django admin support
#### TODO - refactor django widgets, better type-hints, groups access support
## Documentation

```python3
from varorm.models import Model
from varorm import fields
from varorm.storage import JsonStorage
from varorm.exceptions import VarDoesNotExistException

storage = JsonStorage(path="test.json")

class TestModel(Model):
    a = fields.IntegerField(default=1)
    b = fields.CharField(null=True)
    c = fields.FloatField()

TestModel.connect(storage)

print(TestModel().a) # >> 1
print(TestModel().b) # >> None
print(TestModel().c) # >> VarDoesNotExistException

TestModel().a = 5
print(TestModel().a) # >> 5
```

## Django-Documentation
### variables.py in your app(the same where models.py)
```python3
from varorm.models import Model
from varorm import fields

class TestModel(Model):
    a = fields.IntegerField(default=1)
    b = fields.CharField(null=True)
    c = fields.FloatField(verbose_name="Test C")
```
### settings.py
```python3
VARORM_STORAGE = 'varorm.storage.RedisStorage' # import path to storage
VARORM_STORAGE_CONFIG = {
    "url": "redis://localhost:6379/3"
} # storage init config
```
#### Now in your django admin you will find VARORM app, enjoy!
#### Important: when you use FileStorage(JsonStorage or PickleStorage) put {"save_on_set": True} in VARORM_STORAGE_CONFIG