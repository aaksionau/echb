from django import forms
from django.contrib import admin

from .models import Video, VideoCategory, PrayerRequest


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

    def save(self, commit=True):
        instance = super(VideoForm, self).save(commit=False)
        instance.youtube_link = self.change_url(self.instance.youtube_link)
        return instance

    def change_url(self, link):
        if 'embed' not in link:
            return link.replace('/watch?v=', '/embed/')
        else:
            return link


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_link', 'accept_prayer_request', 'category', 'date', 'interesting_event']
    list_filter = ('category',)
    form = VideoForm


admin.site.register(VideoCategory)


@admin.register(PrayerRequest)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'created']
