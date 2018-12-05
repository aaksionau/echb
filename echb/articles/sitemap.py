from django.contrib.sitemaps import Sitemap
from .models import Article


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.modified
