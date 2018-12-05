from django.contrib.sitemaps import Sitemap
from .models import Page


class PagesSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return self.get_full_slug(obj)

    # Recursive loop to get full path
    def get_full_slug(self, page):
        if not page.parent:
            return f"/{page.slug}/"

        return f"{self.get_full_slug(page.parent)}{page.slug}/"
