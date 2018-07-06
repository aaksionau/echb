from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import NewsItem, Event, Author

@admin.register(NewsItem)
class NewsItemAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'
    list_per_page = 40
    date_hierarchy = 'publication_date'
    list_filter = ('published', 'author')
    list_display = ('title', 'published', 'publication_date', 'author')

@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date', 'short_description')

admin.site.register(Author)
