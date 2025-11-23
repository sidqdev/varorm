from django.contrib import admin
from django.urls import path
from django.http import HttpRequest
from varorm.dj import views, globals, utils


def create_varorm_model_admin(groups: list):
    class VarormAdmin(admin.ModelAdmin):
        def has_module_permission(self, _):
            return True
        
        def get_model_perms(self, request):
            return {"view": "__all__" in groups or request.user.is_superuser or request.user.groups.filter(name__in=groups).exists()}

    return VarormAdmin


for app, models in globals.MODELS.items():
    django_model = utils.create_fake_model(app, [x[1] for x in models])
    
    groups = list()
    for model in models:
        model_groups = model[1].get_meta().groups or list()
        if model_groups == '__all__':
            model_groups = ['__all__']
        groups.extend(model_groups)
    groups = list(set(groups))

    admin.site.register(django_model, create_varorm_model_admin(groups))



get_urls = admin.site.get_urls

def custom_get_urls():
    urls = get_urls()
    dj_urls = [
        path("dj/<str:app>/", views.get_app_models),
    ]
    urls = dj_urls + urls
    return urls

admin.site.get_urls = custom_get_urls