from django.urls import path

from . import views

urlpatterns = [
    path('', views.find_church, name='find-church'),
    path('churches.js', views.get_churches, name='churches'),
    path('regions.js', views.get_regions, name='regions'),
    path('geolocation/', views.geolocation, name='geolocation')
]