from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings

import pages.views as pages_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('news/', include('newsevents.urls')),
    path('articles/', include('articles.urls')),
    path('galleries/', include('galleries.urls')),
    path('find-church/', include('churches.urls')),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('?-debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'