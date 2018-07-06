from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import Author, Tag, Article, Category

class ExtraContext(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all().order_by('last_name')
        
        if 'author' in self.kwargs:
            context['chosen_author'] = Author.objects.get(id=self.kwargs['author'])
        elif 'category' in self.kwargs:
            context['chosen_category'] = Category.objects.get(slug=self.kwargs['category'])

        return context

class ArticlesFilterCategoryListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['category'])

class ArticlesFilterAuthorListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(author__id=self.kwargs['author'])

class ArticlesListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.select_related('author', 'category')

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['latest_articles'] = Article.objects.order_by('-date')[:5]
        return data