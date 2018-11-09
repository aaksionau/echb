from unidecode import unidecode

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .managers import GalleryQuerySet


from helpers.models import Audit


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'


class Author(Audit):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'


class Gallery(Audit):
    title = models.CharField(max_length=200)
    date = models.DateField()
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.FileField(upload_to='galleries')
    tags = models.ManyToManyField(Tag, related_name='galleries')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    objects = GalleryQuerySet.as_manager()

    def __str__(self):
        return self.title

    def image_count(self):
        return Image.objects.filter(gallery_id=self.pk).count()

    def get_absolute_url(self):
        return reverse('gallery-detail', kwargs={'slug': self.slug})

    def get_slug(self, title):
        uni_code = unidecode(title).lower()
        slug = slugify(uni_code)
        return slug

    def clean(self):
        slug = self.get_slug(self.title)
        if Gallery.objects.filter(slug=slug).exists():
            raise ValidationError(f'Существует галерея с адресом: {slug}, измените название')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = self.get_slug(self.title)

        super(Gallery, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'
        ordering = ['-date']


def gallery_upload_path(instance, filename):
    return f'galleries/{instance.gallery.slug}/{filename}'


def gallery_upload_path_for_small(instance, filename):
    return f'galleries/{instance.gallery.slug}/small/{filename}'


class Image(Audit):
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to=gallery_upload_path_for_small)
    image = models.FileField(upload_to=gallery_upload_path)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def image_thumb(self):
        return mark_safe(f'<img src="/static/media/{self.thumbnail}" width="100"/>')
    image_thumb.allow_tags = True

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'
