from django.urls import path
from django.views.decorators.cache import cache_page
from echb.settings.base import CACHE_DURATION
from . import views

urlpatterns = [
    path('', cache_page(CACHE_DURATION['extra'])(views.GalleriesListView.as_view()), name='galleries'),
    path('<slug:slug>/', cache_page(CACHE_DURATION['extra'])(views.GalleryDetailView.as_view()), name='gallery-detail'),
    path('archive/<int:year>/', cache_page(CACHE_DURATION['extra'])(views.GalleriesArchiveListView.as_view()), name='galleries-archive'),
    path('filter/tag/<int:tag>/', cache_page(CACHE_DURATION['extra'])(views.GalleriesFilterByTagListView.as_view()), name='galleries-filter-tag'),
    path('filter/author/<int:author>/', cache_page(CACHE_DURATION['extra'])(views.GalleriesFilterByAuthorListView.as_view()), name='galleries-filter-author'),
]