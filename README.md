## varorm - variables orm with django admin support

#### v0.1 - Basic models and Django admin support
#### v0.1.1 - Add groups access to variables and verbose_name for django admin, setup key on init of model
#### v0.1.2 - Add MongoStorage 
#### v0.1.4 - New storage in django model
#### v0.1.5 - Fixed datetime and date fields, added init_load param and update method

#### TODO - refactor django widgets, better type-hints
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

    class Meta: # optional
        key = 'test' # key in storage for current model


TestModel.connect(storage)

print(TestModel().a) # >> 1
print(TestModel().b) # >> None
print(TestModel().c) # >> VarDoesNotExistException

TestModel().a = 5
print(TestModel().a) # >> 5

# Also u can change key in time of using model:
print(TestModel(key='test2').a) # >> 1

storage.save() # for file base storages
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

    class Meta: # optional
        key = 'test' # key in storage for current model
        groups = ['TestGroups'] # groups who have access to this model, __all__ for access to everyone
        verbose_name = 'TestNameOfModel' # the name of model in django admin

```
### settings.py
```python3
INSTALLED_APPS = [
    ...
    "varorm.dj",
    ...
]
VARORM_STORAGE = 'varorm.storage.RedisStorage' # import path to storage
VARORM_STORAGE_CONFIG = {
    "url": "redis://localhost:6379/3"
} # storage init config
```
#### Now in your django admin you will find VARORM app, enjoy!
#### Important: when you use FileStorage(JsonStorage or PickleStorage) put {"save_on_set": True} in VARORM_STORAGE_CONFIG