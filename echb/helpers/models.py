from django.db import models

class Audit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Seo(models.Model):
    seo_keywords = models.CharField(max_length=250, blank=True, null=True)
    seo_description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        abstract=True