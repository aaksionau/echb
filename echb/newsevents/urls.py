from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',  views.NewsListView.as_view(), name='news'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('archive/<int:year>/<int:month>/', views.NewsListView.as_view(), name='archive-news'),
    path('latest/feed/', views.LatestEntriesFeed(), name='news-feed'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('subscriber/success/',
         TemplateView.as_view(template_name='pages/subscription_thankyou.html'),
         name='subscriber-success'),
    path('subscriber/activated/',
         TemplateView.as_view(template_name='pages/subscription_activated.html'),
         name='subscriber-activated'),
    path('subscriber/<uuid:uuid>/', views.ActivateSubscriber.as_view(), name='activate-subscriber'),
    path('subscriber/send-letter/', views.SendLetterToSubscribers.as_view(), name='send_letter'),
    path('subscriber/letter/', views.Letter.as_view(), name='letter'),
]
