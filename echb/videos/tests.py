from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import VideoCategory, Video, PrayerRequest
from pages.models import Page


class VideoTests(TestCase):
    def setUp(self):

        user = User(username='user')
        user.set_password('passphrase')
        user.save()

        add_pages()

        for item in range(2):
            category = VideoCategory.objects.create(
                title=f'test_{item}', slug=f'test-{item}')
            category.save()

        self.client = Client()

    # User can see categories

    def test_user_can_see_links_to_videos(self):
        self.create_video('', True)
        self.create_video('', True)
        response = self.client.get(reverse('online'))

        self.assertContains(response, 'class="video-cat__video-link"', count=2)

    def test_not_auth_user_can_not_send_message(self):
        video = self.create_video('', True)

        data = {'description': 'prayer request'}
        response = self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PrayerRequest.objects.count(), 0)

    def test_message_is_longer_then_250_symbols(self):
        video = self.create_video('', True)
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'passphrase'})
        data = {'description': 'p'*251}

        response = self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.assertContains(response, 'Сообщение должно быть длиной не более')

    def test_user_can_not_send_more_then_2_messages_per_hour(self):
        video = self.create_video('', True)
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'passphrase'})
        data = {'description': 'message'}
        self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.assertEqual(PrayerRequest.objects.count(), 2)

    def test_auth_user_can_send_message(self):
        video = self.create_video('', True)
        self.client.post(reverse('login'), data={'username': 'user', 'password': 'passphrase'})

        data = {'description': 'prayer request'}
        response = self.client.post(
            reverse('video-detail', kwargs={'pk': video.pk}), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PrayerRequest.objects.count(), 1)

    def create_video(self, text, is_feedback, date=timezone.now(), slug='test-0', interesting_event=False):
        video = Video()
        video.title = 'Test0 video'
        video.date = date
        video.youtube_link = 'http://youtube.com'
        video.accept_prayer_request = is_feedback
        if text:
            video.text_for_request = text
        video.category = VideoCategory.objects.filter(slug=slug).first()
        video.interesting_event = interesting_event
        video.save()

        return video


def add_pages():

    for item in ['about-us', 'online', 'thankyou', 'accounts']:
        Page.objects.create(
            title=item, slug=item.lower(), visible_in_menu=True
        )

    accounts = Page.objects.get(slug='accounts')

    Page.objects.create(title='login', slug='login', parent=accounts)
