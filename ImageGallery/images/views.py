from django.shortcuts import render, redirect

from aws import upload_image

from images.forms import UploadFileForm
from images.models import Image

def create(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            if upload_image(file._name, file):

                image = Image.objects.create(
                    name=file._name,
                    content_type=file.content_type,
                    size=file.size,
                    key=file._name,
                )

            return redirect('albums:index')
        else:
            print(form.errors)

    else:
        print('METHOD NOT VALID')