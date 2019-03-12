from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('contacts/', views.ContactsFormView.as_view(), name='contacts'),
    path('contacts/thankyou/', views.ContactsThankYouView.as_view(), name='thankyou'),
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomePageView.as_view(), name='home-page-unique'),
    path('about-us/<slug:parent_slug>/<slug:slug>/',
         views.PageDetailView.as_view(), name='third-level-page'),
    path('about-us/<slug:slug>/', views.PageDetailView.as_view(), name='about-us-page'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt')),
]
