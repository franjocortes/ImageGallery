from django.urls import path

from albums.views import index


app_name = 'albums'

urlpatterns = [
    path('', index, name='index')
]