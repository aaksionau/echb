from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='articles'),
    path('<int:pk>/',
         views.ArticleDetailView.as_view(),
         name='articles-detail'),
    path('filter/category/<slug:category>/',
         views.ArticlesFilterCategoryListView.as_view(),
         name='category-filter'),
    path('filter/author/<int:author>/',
         views.ArticlesFilterAuthorListView.as_view(),
         name='author-filter')
]
