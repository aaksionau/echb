from django.contrib.sitemaps import Sitemap
from .models import NewsItem


class NewsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return NewsItem.objects.all()

    def lastmod(self, obj):
        return obj.modified
