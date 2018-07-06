from django.db import models
from helpers.models import Audit
from django.urls import reverse


class Tag(Audit):
    title = models.CharField(max_length=100)

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

class Category(Audit):
    title = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Author(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
            return self.last_name + ' ' + self.first_name

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

class Article(Audit):
    title = models.CharField(max_length=150)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('articles-detail', args=[self.id])

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-date']
