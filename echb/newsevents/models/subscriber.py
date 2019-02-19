from django.db import models

import uuid

from helpers.models import Audit


class Subscriber(Audit):
    email = models.EmailField(unique=True)
    activated = models.BooleanField(default=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
