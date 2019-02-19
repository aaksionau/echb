from django.contrib import admin

from .models import Video, VideoCategory, PrayerRequest


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_link', 'accept_prayer_request', 'category', 'date', 'interesting_event']
    list_filter = ('category',)


admin.site.register(VideoCategory)


@admin.register(PrayerRequest)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'created']
