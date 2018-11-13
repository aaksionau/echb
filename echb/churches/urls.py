from django.urls import path

from . import views

urlpatterns = [
    path('', views.find_church, name='find-church'),
    path('data/<str:type>', views.get_data, name='map-data')
]
