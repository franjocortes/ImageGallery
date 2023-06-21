from django.db import models
from django.conf import settings

from albums.models import Album


class Image(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    content_type = models.CharField(max_length=20, null=False, blank=False)
    size = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def url(self) -> str:
        bucket_name = getattr(settings, 'AWS_S3_BUCKET_NAME', None)
        root_key = getattr(settings, 'AWS_ROOT_FOLDER', '')
        return f'https://{bucket_name}.s3.amazonaws.com/{root_key + self.key}'

    @property
    def title(self) -> str:
        return self.name.split('.')[0]
    
    @property
    def extension(self) -> str:
        return self.name.split('.')[-1]
    
    def set_name(self, new_name: str) -> None:
        new_name += '.' + self.extension
        new_key = self.album.key + new_name

        if new_key:
            self.key = new_key
            self.name = new_name
            self.save()