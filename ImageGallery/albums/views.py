from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from albums.forms import AlbumForm
from albums.models import Album


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
        album = form.save()
        return redirect('albums:index')
    

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/detail.html'