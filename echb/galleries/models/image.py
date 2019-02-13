from helpers.models import Audit

from django.db import models
from django.utils.html import mark_safe


def gallery_upload_path(instance, filename):
    return f'galleries/{instance.gallery.slug}/{filename}'


def gallery_upload_path_for_small(instance, filename):
    return f'galleries/{instance.gallery.slug}/small/{filename}'


class Image(Audit):
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to=gallery_upload_path_for_small)
    image = models.FileField(upload_to=gallery_upload_path)
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE)

    def image_thumb(self):
        return mark_safe(f'<img src="/static/media/{self.thumbnail}" width="100"/>')
    image_thumb.allow_tags = True

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'
