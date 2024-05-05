from django.contrib import admin
from varorm.dj import views, globals, utils
from django.urls import path


for model_name in globals.MODELS.keys():
    admin.site.register(utils.create_fake_model(model_name))

get_urls = admin.site.get_urls

def custom_get_urls():
    urls = get_urls()
    dj_urls = [
        path("dj/<str:model>/", views.get_app_models),
    ]
    urls = dj_urls + urls
    return urls

admin.site.get_urls = custom_get_urls