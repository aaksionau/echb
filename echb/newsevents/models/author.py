from django.db import models


class Author(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
