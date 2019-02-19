from datetime import datetime, timedelta

from django.db import models
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
