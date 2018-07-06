from django.urls import path
from django.views.decorators.cache import cache_page
from echb.settings.base import CACHE_DURATION
from . import views

urlpatterns = [
    path('', cache_page(CACHE_DURATION['extra'])(views.ArticlesListView.as_view()), name='articles'),
    path('<int:pk>/', cache_page(CACHE_DURATION['extra'])(views.ArticleDetailView.as_view()), name='articles-detail'),
    path('filter/category/<slug:category>/', cache_page(CACHE_DURATION['extra'])(views.ArticlesFilterCategoryListView.as_view()), name='category-filter'),
    path('filter/author/<int:author>/', cache_page(CACHE_DURATION['extra'])(views.ArticlesFilterAuthorListView.as_view()), name='author-filter')
]