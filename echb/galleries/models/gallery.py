from unidecode import unidecode

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError

from helpers.models import Audit

from galleries.managers import GalleryQuerySet

from .image import Image
from .tag import Tag
from .author import Author


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
