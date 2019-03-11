from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core import mail

from .models import Page
from newsevents.models import NewsItem, Event, Author
from articles.models import Article, Category, Author as ArticleAuthor
from galleries.models import Gallery, Author as GalleryAuthor


class PagesTests(TestCase):
    def setUp(self):
        self.client = Client()

        add_pages()

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

        self.assertContains(response, 'class="news-item--home"',
                            count=6)
        self.assertContains(response, 'class="event__title"', count=6)
        self.assertContains(response, 'class="gallery"', count=4)
        self.assertContains(response, 'class="resource--home"', count=6)

    def test_home_page_contains_subscriber_form(self):
        response = self.client.get(reverse('home-page-unique'))
        self.assertContains(response, 'form')

    def test_about_us_page_contains_menu(self):
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

    def test_user_can_send_feedback(self):

        data = {
            'name': 'test',
            'email': 'test@test.ru',
            'subject': 'test',
            'message': 'test'
        }
        response = self.client.post(reverse('contacts'), data=data, follow=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, 'Спасибо за ваше сообщение.')

    def test_feedback_form_send_copy_email_to_user(self):

        data = {
            'name': 'test',
            'email': 'test@test.ru',
            'subject': 'test',
            'message': 'test',
            'cc_myself': True
        }
        response = self.client.post(reverse('contacts'), data=data, follow=True)
        self.assertEqual(len(mail.outbox), 2)  # to admin + user
        self.assertContains(response, 'Спасибо за ваше сообщение.')

    def test_current_page_is_active(self):
        about = Page.objects.get(slug='about-us')
        history = create_page('history', 'churches-history', about)
        create_page('3-level', '3-level', history)
        level_response_1 = self.client.get(reverse('page-detail', kwargs={'slug': 'about-us'}))
        level_response_2 = self.client.get(reverse('about-us-page', kwargs={'slug': 'churches-history'}))
        level_response_3 = self.client.get(reverse('churches-history-page', kwargs={'slug': '3-level'}))
        self.assertContains(level_response_1, 'menu__item menu__item--active')
        self.assertContains(level_response_2, 'menu__item menu__item--active')
        self.assertContains(level_response_3, 'menu__item menu__item--active')

    def test_breadcrumbs(self):
        about_us = Page.objects.get(slug='about-us')
        history = create_page('History', 'churches-history', about_us)
        create_page('3-level', '3-level', history)
        level_response_1 = self.client.get(reverse('page-detail', kwargs={'slug': 'about-us'}))
        level_response_2 = self.client.get(reverse('about-us-page', kwargs={'slug': 'churches-history'}))
        level_response_3 = self.client.get(reverse('churches-history-page', kwargs={'slug': '3-level'}))
        self.assertContains(
            level_response_1, '<a class="breadcrumbs__link" href="/about-us/" title="About-us">About-us</a>')
        self.assertContains(
            level_response_2, '<a class="breadcrumbs__link" href="/about-us/churches-history/" title="History">History</a>')
        self.assertContains(
            level_response_3, '<a class="breadcrumbs__link" href="/about-us/churches-history/3-level/" title="3-level">3-level</a>')


def create_page(title, slug, parent, order=1, visible_in_menu=True):
    page = Page.objects.create(
        title=title, slug=slug, order=order, parent=parent, visible_in_menu=visible_in_menu
    )
    return page


def add_pages():
    for item in ['Home', 'About-us', 'Contacts', 'Thankyou']:
        create_page(item, item.lower(), None)
    about_us = Page.objects.get(slug='about-us')
    for item in ['Online', 'Find-church', 'Galleries']:
        create_page(item, item.lower(), about_us)
