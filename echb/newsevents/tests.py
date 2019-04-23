from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from pages.models import Page
from .models import NewsItem, Author, Subscriber


class NewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.news_per_page = 7

        Page.objects.create(
            title='news', slug='news', order=1, visible_in_menu=True)

        Page.objects.create(
            title='home', slug='home', order=1, visible_in_menu=True)

        now = datetime.now()
        # create newsitem for each month in a year
        for item in range(1, 13):
            news_item = NewsItem()
            news_item.title = f'news item_title'
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
        self.assertContains(response, news_item.title, 14)
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

    def test_user_can_subscribe_to_letter(self):
        response = self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(
            response, 'Ваш email добавлен в список подписчиков')

    def test_subscriber_not_added_if_email_incorrect(self):
        self.client.post(
            reverse('home-page-unique'), data={'email': 'test'})
        self.assertEqual(len(mail.outbox), 0)

    def test_subscriber_can_activate_his_subscription(self):
        self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение о подписке на новости')
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)
        change_url = reverse('activate-subscriber', kwargs={'uuid': subscriber.uuid})
        self.assertIn(change_url, mail.outbox[0].body)
        self.client.get(reverse('activate-subscriber', kwargs={'uuid': subscriber.uuid}))
        subscriber = Subscriber.objects.all().first()
        self.assertTrue(subscriber.activated)

    def test_subscriber_not_activated_with_wrong_uuid(self):
        self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)
        subscriber_uuid = '98194856-4050-4397-9388-396669b5485b'
        self.client.get(reverse('activate-subscriber', kwargs={'uuid': subscriber_uuid}))
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)

    def test_after_subscription_user_get_last_letter(self):
        self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение о подписке на новости')
        subscriber = Subscriber.objects.all().first()
        self.client.get(reverse('activate-subscriber', kwargs={'uuid': subscriber.uuid}))

        subscriber = Subscriber.objects.all().first()
        self.assertTrue(subscriber.activated)

        self.assertEqual(mail.outbox[1].subject, 'Последние новости с сайта ecb.kh.ua')
        self.assertEqual(len(mail.outbox), 2)

    def test_send_several_letters(self):
        for item in range(10):
            subscriber = Subscriber.objects.create(email=f'test_{item}@test.ru', activated=True)
            subscriber.save()

        self.client.get(reverse('send_letter'))
        self.assertEqual(len(mail.outbox), 10)

    def test_letter_was_already_sent_recently(self):
        for item in range(10):
            subscriber = Subscriber.objects.create(email=f'test_{item}@test.ru', activated=True)
            subscriber.save()

        response = self.client.get(reverse('send_letter'))
        self.assertContains(response, 'Letters were successfuly sent')

        response = self.client.get(reverse('send_letter'))
        self.assertContains(response, 'Letters were sent earlier')

        self.assertEqual(len(mail.outbox), 10)
