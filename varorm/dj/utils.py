from typing import Any
from dataclasses import dataclass
from django.conf import settings
from varorm.exceptions import VarDoesNotExistException
from varorm import widgets


def import_by_path(name: str):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def configure_default_setting(default_settings: dict):
    for k, v in default_settings.items():
        try:
            getattr(settings, k)
        except:
            setattr(settings, k, v)


def create_fake_model(name: str, models):
    class FakeMeta:
        abstract            = not True
        app_label           = __name__.split('.')[-2]
        module_name         = None
        verbose_name        = None
        verbose_name_plural = None
        get_ordered_objects = list
        swapped = False
        app_config = ''
        model_name = name
        object_name = name

        def get_add_permission(self):    return 'add_%s'    % self.module_name
        def get_change_permission(self): return 'change_%s' % self.module_name
        def get_delete_permission(self): return 'delete_%s' % self.module_name
        def __init__(self, name, verbose_name=None, verbose_plural=None):
            self.module_name         = name
            self.verbose_name        = verbose_name or name
            self.verbose_name_plural = verbose_plural or name

    class FakeModel:
        varorm_models = models
        _meta = FakeMeta(name)
    
    return [FakeModel]


@dataclass
class FieldAdminRepresintation:
    verbose_name: str
    field_key: str
    value: Any
    widget: widgets.Widget


def get_model_fields_represintation(cls): 
    self = cls()
    fields = []
    for field_key, field in self._fields.items():
        value = None
        try:
            value = getattr(self, field_key)
        except VarDoesNotExistException:
            pass
        fields.append(FieldAdminRepresintation(
            verbose_name=field._verbose_name or field_key.capitalize(),
            field_key=field_key,
            value=value,
            widget=field.widget(field_key, value)
        ))

    return fields


def has_django_model_permission(model, user):
    varorm_models = model.varorm_models
    for varorm_model in varorm_models:
        if has_varorm_model_permission(varorm_model, user):
            return True
        
    return False


def has_varorm_model_permission(model, user):
    if user.is_superuser:
        return True
    groups = model.get_meta().groups
    if groups == "__all__":
        return True
    if groups is None:
        return False
    return bool(set(groups) & set([group.name for group in user.groups.all()]))