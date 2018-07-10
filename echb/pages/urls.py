from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('profile/', views.userprofile, name='profile'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('ministries/', views.MinistryListView.as_view(), name='ministries'),
    path('ministries/<slug:slug>/', views.MinistryDetailView.as_view(), name='ministry-detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/thankyou/',views.thanks, name='thankyou'),
    path('online/', views.videos, name='videos'),
    path('online/<slug:category>', views.videos, name='videos-by-filter'),
    path('prayerrequests/', views.prayerrequests, name='prayer-requests'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home-page-unique'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]