from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse

from pages.models import Page
from .models import NewsItem, Author


class NewsTests(TestCase):
    def setUp(self):
        self.client = Client()

        Page.objects.create(
            title='news', slug='news', order=1, visible_in_menu=True)

        now = datetime.now()
        for item in range(1, 12):
            news_item = NewsItem()
            news_item.title = f'newsitem_title {item}'
            news_item.description = f'news description {item}'
            news_item.author = Author.objects.create(
                last_name='last_name', first_name='news first_name')
            news_item.published = True
            news_item.publication_date = datetime(year=now.year, month=item, day=1)
            news_item.save()

    def test_news_page_is_approachable(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
