from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import NewsItem, Event, Author, Subscriber, MailingLog


@admin.register(NewsItem)
class NewsItemAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'
    list_per_page = 40
    date_hierarchy = 'publication_date'
    list_filter = ('published', 'author')
    list_display = ('title', 'published', 'publication_date', 'author')


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['last_name', ]


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'activated', 'created']


admin.site.register(MailingLog)
