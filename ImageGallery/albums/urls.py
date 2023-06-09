from django.urls import path

from albums.views import index, create


app_name = 'albums'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
]