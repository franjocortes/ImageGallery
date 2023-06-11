from django.forms import Form, FileField, FileInput


class UploadFileForm(Form):
    file = FileField(
        required=True,
        label='Imagen',
        widget=FileInput(
            attrs={'accept': 'image/*'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['file'].widget.attrs['class'] = 'form-control-file'