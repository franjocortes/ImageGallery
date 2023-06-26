from django.urls import path

from images.views import create, update, show, delete


app_name = 'images'

urlpatterns = [
    path('create/', create, name='create'),
    path('update/<int:pk>/', update, name='update'),
    path('show/<int:pk>/', show, name='show'),
    path('delete/<int:pk>/', delete, name='delete'),
]