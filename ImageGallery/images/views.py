from django.shortcuts import render, redirect

from images.forms import UploadFileForm
from images.models import Image

def create(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['file']

            image = Image.objects.create(
                name=image._name,
                content_type=image.content_type,
                size=image.size,
            )

            return redirect('albums:index')
        else:
            print(form.errors)

    else:
        print('METHOD NOT VALID')