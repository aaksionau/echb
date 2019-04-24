from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

from helpers.models import Audit


MESSAGE_LENGTH = 250


class PrayerRequest(Audit):
    description = models.TextField(max_length=500,
                                   validators=[MaxLengthValidator(
                                       limit_value=MESSAGE_LENGTH,
                                       message='Сообщение должно быть длиной не более {}'.format(MESSAGE_LENGTH))])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'молитвенная нужда'
        verbose_name_plural = 'молитвенные нужды'
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
    youtube_link = models.CharField(
        max_length=200, help_text="Cсылка должна быть такого вида: https://www.youtube.com/embed/H0mkJVNmBpM")
    urgent_text = models.CharField(max_length=250, verbose_name="Текст срочного объявления", blank=True, null=True)
    accept_prayer_request = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE)
    interesting_event = models.BooleanField(default=False)
    text_for_request = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,
                                        help_text="Введите название для формы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
        ordering = ['-date']
