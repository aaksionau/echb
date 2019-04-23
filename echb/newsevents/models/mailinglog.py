from django.db import models
from django.utils import timezone


class MailingLog(models.Model):
    date = models.DateField(default=timezone.now)
    emails = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    started = models.TimeField(default=timezone.now)
    finished = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'Рассылка от {self.date.strftime("%d/%m/%y")}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'
