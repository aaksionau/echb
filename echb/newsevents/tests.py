from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse

from pages.models import Page
from .models import NewsItem, Author


class NewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.news_per_page = 7

        Page.objects.create(
            title='news', slug='news', order=1, visible_in_menu=True)

        now = datetime.now()
        # create newsitem for each month in a year
        for item in range(1, 13):
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

    def test_user_can_see_news(self):
        response = self.client.get(reverse('news'))
        self.assertContains(response, 'news-item__title', self.news_per_page)
        self.assertContains(response, 'meta-info__item')
        self.assertContains(response, 'news-item__more', self.news_per_page)
        self.assertContains(response, 'pagination__link', 1)

    def test_user_can_see_archive_on_the_side(self):
        response = self.client.get(reverse('news'))

        self.assertContains(response, 'aside__menu-link', 12)  # full year
        self.assertContains(response, f'Январь {datetime.now().year}')

    def test_user_can_archive_items_on_click(self):
        response = self.client.get(reverse('archive-news', kwargs={'year': datetime.now().year, 'month': 1}))
        self.assertContains(response, 'news-item__title', 1)
        self.assertNotContains(response, 'pagination__item')

    def test_rss_icon(self):
        response = self.client.get(reverse('news'))
        self.assertContains(response, reverse('news-feed'))
        self.assertContains(response, 'rss.png')

    def test_user_can_see_full_news_page(self):
        news_item = NewsItem.objects.first()
        response = self.client.get(reverse('news-detail', kwargs={'pk': news_item.pk}))
        self.assertContains(response, news_item.title, 6)
        self.assertContains(response, 'content__title', 1)
        self.assertContains(response, news_item.author.last_name)
        self.assertContains(response, 'meta-info__item', 2)
        self.assertContains(response, 'news-item__aside-title', 5)

    def test_page_contains_search_input(self):
        response = self.client.get(reverse('news'))
        self.assertContains(response, 'Введите текст для поиска')
        self.assertContains(response, 'search')

    def test_search_page_contains_results(self):
        news_item = NewsItem.objects.first()
        response = self.client.get(f"{reverse('search')}?query={news_item.title}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Результаты поиска')
        self.assertContains(response, 'news-item__link')
        self.assertContains(response, 'news-item__text')

    def test_search_no_results(self):
        response = self.client.get(f"{reverse('search')}?query=query")
        self.assertNotContains(response, 'news-item__link')
        self.assertContains(response, 'Нет записей')
