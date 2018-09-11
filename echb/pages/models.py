from django.db import models
from django.urls import reverse
import uuid
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
    icon = models.FileField(upload_to='video_categories', blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'видео категория'
        verbose_name_plural = 'видео категории'

class Video(Audit):
    title = models.CharField(max_length=150)
    youtube_link = models.CharField(max_length=200)
    urgent_text = models.CharField(max_length=250, verbose_name="Текст срочного объявления", blank=True, null=True)
    accept_prayer_request = models.BooleanField()
    date = models.DateTimeField()
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE)
    interesting_event = models.BooleanField(default=False)
    text_for_request = models.CharField(max_length=200, blank=True, null=True, help_text="Введите текст для формы, по умолчанию: Здесь вы можете оставить молитвенную записку, чтобы во время служения Церковь могла молится за Вашу нужду.")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
        ordering = ['date']

class Subscriber(Audit):
    email = models.EmailField(unique=True)
    activated = models.BooleanField(default=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'

class OldUser(models.Model):
    login = models.CharField(max_length=100)
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    email = models.EmailField()

    def __str__(self):
        return self.email
