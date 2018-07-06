from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Page, Ministry, Feedback, Video, VideoCategory, PrayerRequest

@admin.register(Page)
class AdminPage(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'order', 'parent', 'visible_in_menu', 'created', 'modified')
    list_filter = ('parent',)

@admin.register(Ministry)
class MinistryAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'short_description','created', 'modified',)
    summernote_fields = ('description',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'name', 'created']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_link', 'accept_prayer_request', 'category', 'date']
    list_filter = ('category',)
    
admin.site.register(VideoCategory)
admin.site.register(PrayerRequest)