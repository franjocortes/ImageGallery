from django.urls import path

from albums.views import create
from albums.views import AlbumListView, AlbumDetailView


app_name = 'albums'

urlpatterns = [
    path('', AlbumListView.as_view(), name='index'),
    path('create/', create, name='create'),
    path('<int:pk>/detail', AlbumDetailView.as_view(), name='detail'),
]