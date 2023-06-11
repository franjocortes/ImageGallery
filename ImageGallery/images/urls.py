from django.urls import path

from images.views import create


app_name = 'images'

urlpatterns = [
    path('create/', create, name='create'),
]