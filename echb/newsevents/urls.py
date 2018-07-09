from django.urls import path
from django.views.decorators.cache import cache_page
from echb.settings.base import CACHE_DURATION
from . import views

urlpatterns = [
    path('',  cache_page(CACHE_DURATION['light'])(views.NewsListView.as_view()), name='news'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('archive/<int:year>/<int:month>/', cache_page(CACHE_DURATION['extra'])(views.NewsListView.as_view()), name='archive-news'),
    path('latest/feed/', views.LatestEntriesFeed(), name='news-feed'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
]
