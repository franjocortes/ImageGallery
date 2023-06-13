from django.shortcuts import render, redirect, get_object_or_404

from aws import upload_image

from albums.models import Album

from images.forms import UploadFileForm
from images.models import Image

def create(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            album = get_object_or_404(Album, pk=form.cleaned_data['album_id'])

            key = album.key + file._name
            
            if upload_image(key, file):

                image = Image.objects.create(
                    name=file._name,
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