from django.shortcuts import render
from django.http import HttpRequest
from varorm.dj.globals import MODELS
from varorm.dj import utils

def get_app_models(request: HttpRequest, app: str):
    if request.method == 'POST':
        data = dict(request.POST)
        model_name = data['dj.model_name'][0]
        field_key = data['dj.field_key'][0]
        value = data[field_key][0]
        for mn, m in MODELS[app]:
            if mn == model_name and utils.has_varorm_model_permission(m, request.user):
                setattr(m(), field_key, value)
                break

    return render(request, "models_list.html", {
        "models": [
            (v.get_meta().verbose_name or k, utils.get_model_fields_represintation(v)) 
            for k, v in MODELS[app] 
            if utils.has_varorm_model_permission(v, request.user)
        ]
    })

