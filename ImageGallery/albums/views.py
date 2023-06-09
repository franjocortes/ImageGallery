from django.shortcuts import render, redirect

from albums.forms import AlbumForm
from albums.models import Album


def index(request):
    form = AlbumForm()
    albums = Album.objects.all()
    context = {
        'title': 'Gallery',
        'form': form,
        'albums': albums,
    }
    return render(request, 'albums/list.html', context)


def create(request):
    form = AlbumForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        album = form.save()
        return redirect('albums:index')