from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.sitemaps.views import sitemap

from django.conf import settings

from pages.sitemap import PagesSitemap
from newsevents.sitemap import NewsSitemap
from articles.sitemap import ArticleSitemap

sitemaps = {
    'pages': PagesSitemap,
    'news': NewsSitemap,
    'articles': ArticleSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('news/', include('newsevents.urls')),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
    path('about-us/galleries/', include('galleries.urls')),
    path('about-us/find-church/', include('churches.urls')),
    path('', include('pages.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('?-debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'
