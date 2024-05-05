import inspect
from django.conf import settings

from varorm.storage import BaseStorage
from varorm.models import Model
from varorm.dj import utils
from varorm.dj import globals


utils.configure_default_setting({
    "VARORM_STORAGE": "varorm.storage.MemoryStorage",
    "VARORM_STORAGE_CONFIG": {}
})

storage = utils.import_by_path(settings.VARORM_STORAGE)(**settings.VARORM_STORAGE_CONFIG)
assert isinstance(storage, BaseStorage)


models = dict()

for app in settings.INSTALLED_APPS:
    try:
        module = __import__(f"{app}.variables")
        module = getattr(module, 'variables')
    except:
        continue

    for i in inspect.getmembers(module, inspect.isclass):
        if issubclass(i[1], Model) and i[1] is not Model:
            i[1].connect(storage)
            if app in models:
                models[app].append(i)
            else:
                models[app] = [i]

globals.MODELS = models
