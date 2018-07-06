from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Region, Church

@admin.register(Church)
class NewsItemAdmin(SummernoteModelAdmin):
    list_per_page = 20
    list_filter = ('region',)
    list_display = ('title', 'address', 'region', 'website','email','lat','lng')

admin.site.register(Region)

