from django.db import models
from django.urls import reverse

from helpers.models import Audit


class Event(Audit):
    title = models.CharField(max_length=150)
    date = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    short_description = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', args=[self.id])

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'
