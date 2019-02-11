from django.urls import path
from . import views

urlpatterns = [
    path('',  views.NewsListView.as_view(), name='news'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('archive/<int:year>/<int:month>/', views.NewsListView.as_view(), name='archive-news'),
    path('latest/feed/', views.LatestEntriesFeed(), name='news-feed'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('search/', views.SearchListView.as_view(), name='search'),
]
