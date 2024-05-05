from django.shortcuts import render
from django.http import HttpRequest
from varorm.dj.globals import MODELS
from varorm.dj import utils

def get_app_models(request: HttpRequest, model: str):
    if request.method == 'POST':
        data = dict(request.POST)
        model_name = data['dj.model_name'][0]
        field_key = data['dj.field_key'][0]
        value = data[field_key][0]
        for mn, m in MODELS[model]:
            if mn == model_name:
                setattr(m(), field_key, value)
                break

    return render(request, "models_list.html", {
        "models": [(k, utils.get_model_fields_represintation(v)) for k, v in MODELS[model]]
    })

