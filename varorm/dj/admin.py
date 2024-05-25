from django.contrib import admin
from django.urls import path
from django.http import HttpRequest

from varorm.dj import views, globals, utils

    
class VarormAdmin(admin.ModelAdmin):
        def has_module_permission(self, _):
            return True
        
        def get_model_perms(self, _):
            return {"view": True}

for app, models in globals.MODELS.items():
    django_model = utils.create_fake_model(app, [x[1] for x in models])
    admin.site.register(django_model, VarormAdmin)


_build_app_dict = admin.site._build_app_dict

def custom_build_app_dict(request: HttpRequest, label=None):
    app_dict = _build_app_dict(request, label)
    if 'dj' in app_dict:
        models = app_dict['dj']['models']
        models = list(filter(lambda x: utils.has_django_model_permission(x['model'], request.user), models))
        if len(models) == 0:
            del app_dict['dj']
        else:
            app_dict['dj']['models'] = models

    return app_dict

admin.site._build_app_dict = custom_build_app_dict


get_urls = admin.site.get_urls

def custom_get_urls():
    urls = get_urls()
    dj_urls = [
        path("dj/<str:app>/", views.get_app_models),
    ]
    urls = dj_urls + urls
    return urls

admin.site.get_urls = custom_get_urls