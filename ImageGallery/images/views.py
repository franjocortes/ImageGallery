from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

from aws import upload_image, delete_file, get_file_content

from albums.models import Album

from images.forms import UploadFileForm
from images.models import Image


def show(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return JsonResponse({
        'id': image.pk,
        'name': image.name,
        'delete_url': reverse('images:delete', kwargs={'pk': image.pk})
    })


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


def delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    album = image.album

    if delete_file(image.key):
        image.delete()

    return redirect('albums:detail', album.id)


def download(request, pk):
    image = get_object_or_404(Image, pk=pk)
    content = get_file_content(image.key)
    if content:
        response = HttpResponse(content, content_type=image.content_type)
        response['Content-Disposition'] = f'attachment; filename={image.name}'
        return response
    print('ERROR: an error with aws s3')
    return redirect('albums:detail', image.album.id)

