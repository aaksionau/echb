from django.db import models
from django.contrib.auth.models import User

from helpers.models import Audit


class PrayerRequest(Audit):
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'молитвенная нужда'
        verbose_name_plural = 'молитвенные нужды'
        ordering = ['created']
