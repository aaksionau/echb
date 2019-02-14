from datetime import datetime
from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Article, Author, Tag, Category
from pages.models import Page


class ArticleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_per_page = 5

        Author.objects.create(last_name='author 1', first_name='testovich')
        Author.objects.create(last_name='author 2', first_name='testovich')

        Category.objects.create(title='Category 1', slug='cat-1')
        Category.objects.create(title='Cat 2', slug='cat-2')

        Page.objects.create(
            title='articles', slug='articles', order=1, visible_in_menu=True)

        now = datetime.now()
        # create newsitem for each month in a year
        for item in range(1, 10):
            article = Article()
            article.title = f'article_title {item}'
            article.description = f'article description {item}'
            article.category = Category.objects.first()
            article.author = Author.objects.first()
            article.date = datetime(year=now.year, month=item, day=1)
            article.save()

    def test_article_page_can_be_opened(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)

    def test_articles_list_available(self):
        response = self.client.get(reverse('articles'))
        self.assertContains(response, 'resource__title', self.articles_per_page)
        self.assertContains(response, 'article_title')
        self.assertContains(response, 'pagination__link')
        self.assertContains(response, 'Страница 1 из 2.')
        next_page = self.client.get('{}?page={}'.format(reverse('articles'), 2))
        self.assertContains(next_page, 'article_title')
        self.assertContains(response, 'Категории')
        self.assertContains(response, 'author 1 testovich')
        self.assertContains(response, 'Category 1')

    def test_article_page_available(self):
        response = self.client.get(reverse('articles-detail', kwargs={'pk': 1}))
        self.assertContains(response, 'article_title')
        self.assertContains(response, 'Category 1')
        self.assertContains(response, 'author 1 testovich')
        self.assertContains(response, 'meta-info__item', 3)
        self.assertContains(response, 'Последние статьи')
        self.assertContains(response, 'resource__aside-title', 5)
