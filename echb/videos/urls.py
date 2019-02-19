from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.CurrentVideosListView.as_view(), name='online'),
    path('thankyou/', TemplateView.as_view(template_name="videos/prayer_thankyou.html"), name='video-detail-thankyou'),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('interesting-events/', views.VideoListView.as_view(), name='interesting-videos'),
]
