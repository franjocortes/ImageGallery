from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title': 'Listado de albums'
    }
    return render(request, 'albums/list.html', context)