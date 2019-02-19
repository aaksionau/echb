from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('contacts/', views.ContactsFormView.as_view(), name='contacts'),
    path('contacts/thankyou/', views.ContactsThankYouView.as_view(), name='thankyou'),
    path('subscriber/success/',
         TemplateView.as_view(template_name='pages/subscription_thankyou.html'),
         name='subscriber-success'),
    path('subscriber/activated/',
         TemplateView.as_view(template_name='pages/subscription_activated.html'),
         name='subscriber-activated'),
    path('activate-subscriber/<uuid:uuid>/', views.ActivateSubscriber.as_view(), name='activate-subscriber'),
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomePageView.as_view(), name='home-page-unique'),
    path('about-us/churches-history/<slug:slug>/', views.PageDetailView.as_view(), name='churches-history-page'),
    path('about-us/<slug:slug>/', views.PageDetailView.as_view(), name='about-us-page'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
    path('send-letter', views.SendLetterToSubscribers.as_view(), name='send_letter'),
    path('letter', views.Letter.as_view(), name='letter'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt')),
]
