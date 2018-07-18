from django.contrib import admin

from .models import PrayerRequest

@admin.register(PrayerRequest)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'created']