from dataclasses import dataclass
from django import forms
from varorm import fields
from varorm.models import Model
from varorm.exceptions import *


@dataclass
class FieldAdminRepresintation:
    field_key: str
    form: forms.Form


class VarORMAdmin:
    def __init__(self, model: Model):
        self.model = model
    
    def _generate_form(self, field: fields.Field, field_key, initial, ) -> forms.Field:
        context = dict(
            label=field._verbose_name or field_key.capitalize(),
            initial=initial,
            required=field._null,
            **(field.form_field_extra_context or {})
        )
        form_field = None
        if field._choices is not None:
            form_field = forms.ChoiceField(
                choices=field._choices, 
                **context
            )
        elif isinstance(field, fields.IntegerField):
            form_field = forms.IntegerField(
                **context
            )
        elif isinstance(field, fields.DateTimeField):
            form_field = forms.DateTimeField(
                widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
                **context,
            )
        elif isinstance(field, fields.FloatField):
            form_field = forms.FloatField(
                **context
            )
        elif isinstance(field, fields.BooleanField):
            choices = [
                (True, "Yes"),
                (False, "No")
            ]
            if field._null:
                choices.append(("-", None))
            form_field = forms.ChoiceField(
                choices=choices,
                **context,
            )
        elif isinstance(field, fields.CharField):
            form_field = forms.CharField(
                **context
            )
        elif isinstance(field, fields.TextField):
            form_field = forms.CharField(
                widget=forms.Textarea(),
                **context,
            )
        elif isinstance(field, fields.DateField):
            form_field = forms.DateField(
                widget=forms.DateInput(attrs={"type": "date"}),
                **context,
            )
        
        class Form(forms.Form):
            f = form_field

        return FieldAdminRepresintation(
            field_key=field_key,
            form=Form
        )
        

    def get_forms(self):
        fields = []
        for field_key, field in self.model._fields.items():
            value = None
            try:
                value = getattr(self.model, field_key)
            except VarDoesNotExistException:
                pass
            fields.append(self._generate_form(field, field_key, value))

        return fields