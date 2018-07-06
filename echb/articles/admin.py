from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Author, Tag, Article, Category

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title','date','category', 'author')
    list_filter = ('category', 'author')
    list_per_page = 20

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
