from django.shortcuts import render

from albums.forms import AlbumForm

# Create your views here.

def index(request):
    form = AlbumForm()
    context = {
        'title': 'Gallery',
        'form': form,
    }
    return render(request, 'albums/list.html', context)