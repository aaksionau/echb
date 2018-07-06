from django.db import models

from helpers.models import Audit

class Region(Audit):
    name = models.CharField(max_length=150)
    city_img = models.FileField(upload_to='regions')

    def __str__(self):
            return self.name

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'
        ordering = ['name']

class Church(Audit):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    tel = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=30, null=True, blank=True)
    schedule = models.TextField(null=True, blank=True)
    img = models.FileField(upload_to='churches', null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    lat = models.CharField(max_length=20, null=True, blank=True)
    lng = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = 'церковь'
        verbose_name_plural = 'церкви'
        ordering = ['title']