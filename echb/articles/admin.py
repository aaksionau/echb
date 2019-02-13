from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Author, Category, Tag, Comment


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date', 'category', 'author')
    list_filter = ('category', 'author')
    list_per_page = 20


admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
