from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from helpers.models import Audit, Seo

class Page(Audit, Seo):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    parent = models.ForeignKey('Page', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True)
    visible_in_menu = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'страница сайта'
        verbose_name_plural = 'страницы сайта'

class Ministry(Audit, Seo):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    description = models.TextField(null=True, blank=True)
    icon = models.FileField(upload_to='ministries')

    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('ministry-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'служение'
        verbose_name_plural = 'служения'

class Feedback(Audit):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    cc_myself = models.BooleanField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['created']

class VideoCategory(Audit):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'видео категория'
        verbose_name_plural = 'видео категории'

class Video(Audit):
    title = models.CharField(max_length=150)
    youtube_link = models.CharField(max_length=200)
    accept_prayer_request = models.BooleanField()
    date = models.DateTimeField()
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
        ordering = ['date']

class PrayerRequest(Audit):
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'молитвенная нужда'
        verbose_name_plural = 'молитвенные нужды'
        ordering = ['created']
