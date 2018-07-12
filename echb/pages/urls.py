from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('ministries/', views.MinistryListView.as_view(), name='ministries'),
    path('ministries/<slug:slug>/', views.MinistryDetailView.as_view(), name='ministry-detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/thankyou/',views.thanks, name='thankyou'),
    path('online/', views.videos, name='videos'),
    path('online/<slug:category>', views.videos, name='videos-by-filter'),
    path('prayerrequests/', views.prayerrequests, name='prayer-requests'),
    path('activate-subscriber/<uuid:uuid>/', views.activate_subscriber, name='activate-subscriber'),
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomePageView.as_view(), name='home-page-unique'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]