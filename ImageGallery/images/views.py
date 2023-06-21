from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse

from aws import upload_image

from albums.models import Album

from images.forms import UploadFileForm
from images.models import Image


def update(request, pk):
    
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=pk)
        new_name = request.POST.get('name', '')
        image.set_name(new_name)

        return JsonResponse({
            'id': image.id,
            'name': image.title,
            'url': image.url
        })
    
    return JsonResponse({
        'id': None,
        'name': None,
        'url': None
    })
    

def create(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            album = get_object_or_404(Album, pk=form.cleaned_data['album_id'])

            file_name = file._name.lower().replace(' ', '_')
            key = album.key + file_name
            
            if upload_image(key, file):

                image = Image.objects.create(
                    name=file_name,
                    content_type=file.content_type,
                    size=file.size,
                    key=key,
                    album=album
                )

            return redirect('albums:detail', album.pk)
        else:
            print(form.errors)

    else:
        print('METHOD NOT VALID')
