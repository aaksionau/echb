from datetime import datetime
from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import Article, Author, Tag, Category, Comment
from pages.models import Page


class ArticleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_per_page = 5

        Author.objects.create(last_name='author 1', first_name='testovich')
        Author.objects.create(last_name='author 2', first_name='testovich')

        Category.objects.create(title='Category 1', slug='cat-1')
        Category.objects.create(title='Cat 2', slug='cat-2')

        user = User(username='user', email='test@test.com')
        user.set_password('passphrase')
        user.save()

        Page.objects.create(
            title='articles', slug='articles', order=1, visible_in_menu=True)

        self.now = datetime.now()
        for item in range(1, 10):
            article = Article()
            article.title = f'article_title_{item}'
            article.description = f'article_description_{item}'
            article.category = Category.objects.first()
            article.author = Author.objects.first()
            article.date = datetime(year=self.now.year, month=item, day=1)
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
        url, article = self.get_url_and_article()
        response = self.client.get(url)
        self.assertContains(response, article.title)
        self.assertContains(response, article.description)
        self.assertContains(response, article.category)
        self.assertContains(response, article.author)
        self.assertContains(response, 'meta-info__item', 4)
        self.assertContains(response, 'Последние статьи')
        self.assertContains(response, 'resource__aside-title', 5)

    def test_article_contains_form_for_comments_for_authenticated_user(self):
        url, article = self.get_url_and_article()
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'passphrase'})
        response = self.client.get(url)
        self.assertContains(response, 'id_body')

    def test_article_contains_form_for_comments_for_non_authenticated_user(self):
        url, article = self.get_url_and_article()
        response = self.client.get(url)
        self.assertContains(response, 'id_name')
        self.assertContains(response, 'id_email')
        self.assertContains(response, 'id_body')

    def test_auth_user_can_comment_article(self):
        url, article = self.get_url_and_article()

        comment_data = {'body': 'Text message'}
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'passphrase'})
        self.client.post(url, data=comment_data)

        self.assertEqual(Comment.objects.count(), 1)

    def test_non_auth_user_can_comment_article(self):
        url, article = self.get_url_and_article()
        comment_data = {'name': 'alex',
                        'email': 'test@test.ru',
                        'body': 'Text message'
                        }
        self.client.post(url, data=comment_data)
        self.assertEqual(Comment.objects.count(), 1)

    def test_no_comments(self):
        url, article = self.get_url_and_article()

        response = self.client.get(url)
        self.assertContains(response, 'Комментарии')
        self.assertContains(response, 'Данную статью еще никто не комментировал. Вы можете быть первыми.')

    def test_user_can_see_list_of_comments(self):
        url, article = self.get_url_and_article()
        user = User.objects.first()
        for i in range(4):
            Comment.objects.create(article=article, name=user.username,
                                   email=user.email, body='Comment_message_{}'.format(i))

        response = self.client.get(url)

        self.assertContains(response, 'Comment_message', 4)
        self.assertContains(response, 'Пользователь: user', 4)

    def test_not_active_comments_not_visible(self):
        url, article = self.get_url_and_article()
        user = User.objects.first()
        Comment.objects.create(article=article, name=user.username,
                               active=False,   email=user.email, body='Not active message')

        response = self.client.get(url)

        self.assertNotContains(response, 'Not active message')

    def test_article_contains_comments_count(self):
        url, article = self.get_url_and_article()
        Comment.objects.create(article=article, name='test', email='email@email.com', body='Active message')
        response = self.client.get(url)
        self.assertContains(response, 'Комментарии ({})'.format(Comment.objects.count()))

    def test_every_article_contains_comment_count(self):
        article = Article.objects.first()
        Comment.objects.create(article=article, name='test', email='email@email.com', body='Active message')
        Comment.objects.create(article=article, name='test', email='email@email.com', body='Active message')
        response = self.client.get(reverse('articles'))
        self.assertContains(response, article.title)
        self.assertContains(response, 'Комментарии (2)')

    def get_url_and_article(self):
        article = Article.objects.first()
        url = reverse('articles-detail', kwargs={'pk': article.pk})
        return url, article
