from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import RedirectView, TemplateView


from . import views

urlpatterns = [
    path('ministries/', views.MinistryListView.as_view(), name='ministries'),
    path('ministries/<slug:slug>/', views.MinistryDetailView.as_view(), name='ministry-detail'),
    path('contacts/', views.ContactsFormView.as_view(), name='contacts'),
    path('contacts/thankyou/',views.ContactsThankYouView.as_view(), name='thankyou'),
    path('online/', RedirectView.as_view(url='/online/preobrazhenie/')),
    path('online/preobrazhenie/', views.VideoDetailView.as_view(), name='video-preobrazhenie'),
    path('online/preobrazhenie/thankyou/', views.TemplateView.as_view(template_name="pages/prayer_thankyou.html"), name='video-preobrazhenie-thankyou'),
    path('online/<slug:category>/', views.VideoListView.as_view(), name='videos-by-filter'),
    path('subscriber/success/', TemplateView.as_view(template_name='pages/subscription_thankyou.html'), name='subscriber-success'),
    path('subscriber/activated/', TemplateView.as_view(template_name='pages/subscription_activated.html'), name='subscriber-activated'),
    path('activate-subscriber/<uuid:uuid>/', views.ActivateSubscriber.as_view(), name='activate-subscriber'),
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomePageView.as_view(), name='home-page-unique'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]