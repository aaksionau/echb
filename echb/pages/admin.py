from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Page, Feedback, OldUser


@admin.register(Page)
class AdminPage(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'order', 'parent', 'visible_in_menu', 'created', 'modified')
    list_filter = ('parent',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'name', 'created']


admin.site.register(OldUser)
