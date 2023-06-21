from django.urls import path

from images.views import create, update


app_name = 'images'

urlpatterns = [
    path('create/', create, name='create'),
    path('update/<int:pk>/', update, name='update'),
]