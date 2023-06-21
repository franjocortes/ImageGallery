from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.conf import settings

from albums.forms import AlbumForm
from albums.models import Album

from images.forms import UploadFileForm


class AlbumListView(ListView):
    model = Album
    template_name = 'albums/list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Gallery'
        context['form'] = AlbumForm()

        return context


def create(request):
    form = AlbumForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        album = Album.objects.create_by_aws(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'])

        return redirect('albums:index')
    

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = self.get_object().title
        context['form'] = UploadFileForm({
            'album_id': self.get_object().pk
        })
        context['images'] = self.get_object().images
        context['aws'] = {
            'bucket_name': getattr(settings, 'AWS_S3_BUCKET_NAME', None),
            'root_key': getattr(settings, 'AWS_ROOT_FOLDER', '')
        }

        return context