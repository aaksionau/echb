from django.db import models
from django.utils import timezone
from django.urls import reverse

from helpers.models import Audit

class Author(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    def __str__(self):
            return self.last_name + ' ' + self.first_name

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

class NewsItem(Audit):
    title = models.CharField(max_length=150, help_text="Введите название в нижнем регистре (кроме первой буквы)")
    published = models.BooleanField(default=True)
    publication_date = models.DateTimeField()
    main_image = models.FileField(upload_to='news', null=True, blank=True, help_text="Маленькое изображение, которое будет появляться около новости")
    short_description = models.TextField(null=True, blank=True, help_text="Краткое описание новости")
    description = models.TextField(null=True, blank=True, help_text="Проверяйте орфографию <a href='https://advego.com/text/'>здесь</a>")
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args=[self.id])

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['publication_date']


class Event(Audit):
    title = models.CharField(max_length=150)
    date = models.DateField()
    short_description = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', args=[self.id])

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'