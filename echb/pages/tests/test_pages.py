from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core import mail

from ..models import Page, Subscriber
from newsevents.models import NewsItem, Event, Author
from articles.models import Article, Category, Author as ArticleAuthor
from galleries.models import Gallery, Author as GalleryAuthor


class PagesTests(TestCase):
    def setUp(self):
        self.client = Client()

        Page.objects.create(
            title='home', slug='home', order=1, visible_in_menu=True)

        for item in range(12):
            news_item = NewsItem()
            news_item.title = f'newsitem_title {item}'
            news_item.description = f'news description {item}'
            news_item.author = Author.objects.create(
                last_name='last_name', first_name='news first_name')
            news_item.published = True
            news_item.publication_date = timezone.now()
            news_item.save()

        for item in range(6):
            event = Event()
            event.title = f'event_title {item}'
            event.date = timezone.now() + timedelta(days=1)
            event.short_description = f'desciption {item}'
            event.save()

        for item in range(6):
            gallery = Gallery()
            gallery.title = f'gallery_title {item}'
            gallery.author = GalleryAuthor.objects.create(
                last_name='last_name', first_name='gallery first_name')
            gallery.date = timezone.now()
            gallery.save()

        for item in range(6):
            article = Article()
            article.title = f'article_title {item}'
            article.date = timezone.now()
            article.category = Category.objects.create(
                title='category', slug='slug-0')
            article.author = ArticleAuthor.objects.create(
                last_name='last_name', first_name='article first_name')
            article.save()

    def test_404_page(self):
        response = self.client.get(reverse('page-detail', kwargs={'slug': 'about'}))
        self.assertContains(response, 'Запрошенная страница не найдена.', status_code=404)

    def test_home_page_has_news_events_articles_galleries(self):
        response = self.client.get(reverse('home-page-unique'))

        self.assertContains(response, 'newsitem_title',
                            count=18)  # 6 total (exclude title)
        self.assertContains(response, 'event_title', count=12)  # 6 total
        self.assertContains(response, 'photo-content', count=4)  # 4 total
        self.assertContains(response, 'article_title', count=12)  # 6 total

    def test_home_page_contains_subscriber_form(self):
        response = self.client.get(reverse('home-page-unique'))
        self.assertContains(response, 'form')
    """
    def test_user_can_subscribe_to_letter(self):
        response = self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(
            response, 'Ваш email добавлен в список подписчиков')
    
    def test_subscriber_not_added_if_email_incorrect(self):
        response = self.client.post(
            reverse('home-page-unique'), data={'email': 'test'})
        self.assertEqual(len(mail.outbox), 0)

    def test_subscriber_can_activate_his_subscription(self):
        response = self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение о подписке на новости')
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)
        change_url = reverse('activate-subscriber', kwargs={'uuid':subscriber.uuid})
        self.assertIn(change_url, mail.outbox[0].body)
        self.client.get(reverse('activate-subscriber', kwargs={'uuid':subscriber.uuid}))
        subscriber = Subscriber.objects.all().first()
        self.assertTrue(subscriber.activated)

    def test_subscriber_not_activated_with_wrong_uuid(self):
        self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)
        subscriber_uuid = '98194856-4050-4397-9388-396669b5485b'
        self.client.get(reverse('activate-subscriber', kwargs={'uuid':subscriber_uuid}))
        subscriber = Subscriber.objects.all().first()
        self.assertFalse(subscriber.activated)

    def test_after_subscription_user_get_last_letter(self):
        response = self.client.post(
            reverse('home-page-unique'), data={'email': 'test@test.ru'})
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение о подписке на новости')
        subscriber = Subscriber.objects.all().first()
        self.client.get(reverse('activate-subscriber', kwargs={'uuid':subscriber.uuid}))

        subscriber = Subscriber.objects.all().first()
        self.assertTrue(subscriber.activated)

        self.assertEqual(mail.outbox[1].subject, 'Последние новости с сайта ecb.kh.ua')
        self.assertEqual(len(mail.outbox), 2)
    """

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

    def test_about_us_page_contains_menu(self):
        Page.objects.create(
            title='parent', slug='about-us', order=1, visible_in_menu=True)
        Page.objects.create(
            title='child', slug='child-about-us', order=2, visible_in_menu=True)
        Page.objects.create(
            title='church', slug='churches-history', order=2, visible_in_menu=True)
        Page.objects.create(
            title='church child', slug='churches-history-child', order=2, visible_in_menu=True)

        response = self.client.get(
            reverse('page-detail', kwargs={'slug': 'about-us'}))
        self.assertContains(response, 'child-about-us')
        self.assertContains(response, 'churches-history-child')
    """
    def test_user_can_send_feedback(self):
        contacts = Page.objects.create(
            title='contacts', slug='contacts', order=1, visible_in_menu=True)

        data = {
            'name': 'test',
            'email':'test@test.ru',
            'subject':'test',
            'message': 'test'
        }
        response = self.client.post(reverse('contacts'), data=data, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, 'Спасибо за ваше сообщение.')

    def test_feedback_form_send_copy_email_to_user(self):
        contacts = Page.objects.create(
            title='contacts', slug='contacts', order=1, visible_in_menu=True)

        data = {
            'name': 'test',
            'email':'test@test.ru',
            'subject':'test',
            'message': 'test',
            'cc_myself': True
        }
        response = self.client.post(reverse('contacts'), data=data, follow=True)
        self.assertEqual(len(mail.outbox), 2) #to admin + user
        self.assertContains(response, 'Спасибо за ваше сообщение.')
    """
