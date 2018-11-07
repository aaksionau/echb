from datetime import timedelta
import random
import string

from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import VideoCategory, Video


class VideoTests(TestCase):
    def setUp(self):

        user = User(username='user')
        user.set_password('passphrase')
        user.save()

        for item in range(2):
            category = VideoCategory.objects.create(
                title=f'test_{item}', slug=f'test-{item}')
            category.save()

        self.client = Client()

    def test_interesting_events_include_only_video_with_interesting_checked(self):
        self.create_video('', False, interesting_event=True)
        response = self.client.get(reverse('interesting-videos'))
        self.assertContains(response, 'Test0 video')  # video title

    def test_interesting_events_dont_show_video_without_interesting_checked(self):
        self.create_video('', False, interesting_event=False)
        response = self.client.get(reverse('interesting-videos'))
        self.assertNotContains(response, 'Test0 video')  # video title

    def test_not_authorised_user_can_see_login_and_register_buttons(self):
        self.create_video('', False)

        response = self.client.get(
            reverse('videos-by-filter', kwargs={'slug': 'test-0'}))
        self.assertContains(response, 'Вход')
        self.assertContains(response, 'Регистрация')

    def test_check_categories_displayed_when_video_date_is_less_then_7_days(self):
        time_delta = timezone.now() - timedelta(days=1)
        self.create_video('', False, time_delta, 'test-0')
        self.create_video('', False, time_delta, 'test-1')

        response = self.client.get(reverse('online'))
        self.assertContains(response, 'test_0')  # category title
        self.assertContains(response, 'test_1')  # category title

    def test_check_there_are_no_catefgories_if_videos_are_older_then_7_days(self):
        time_delta = timezone.now() - timedelta(days=8)
        self.create_video('', False, time_delta, 'test-0')
        self.create_video('', False, time_delta, 'test-1')

        response = self.client.get(reverse('online'))
        self.assertContains(
            response, 'За прошедшие 7 дней не было онлайн трансляций.')

    def test_authorised_user_can_see_feedback_form(self):
        self.create_video('', True)

        self.client.login(username='user', password='passphrase')
        response = self.client.get(
            reverse('videos-by-filter', kwargs={'slug': 'test-0'}))

        self.assertContains(
            response, 'Оставьте молитвенную записку, чтобы во время служения Церковь могла молиться за Вашу нужду.')

    def test_authorized_user_redirect_to_thank_you_page(self):
        self.create_video('', True)
        self.client.login(username='user', password='passphrase')
        response = self.client.post(reverse(
            'videos-by-filter', kwargs={'slug': 'test-0'}), data={'description': 'Тестовая запись'})
        self.assertRedirects(response, reverse(
            'video-detail-thankyou', kwargs={'slug': 'test-0'}))

    def test_authorized_user_will_see_error_if_feedback_is_too_long(self):
        self.create_video('', True)
        self.client.login(username='user', password='passphrase')
        text = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=300))

        response = self.client.post(reverse(
            'videos-by-filter', kwargs={'slug': 'test-0'}), data={'description': text}, follow=True)
        self.assertTemplateUsed(response, 'pages/video_detail.html')
        self.assertContains(
            response, 'Ваше сообщение слишком длинное. Максимум 250 символов.')

    def test_not_authorized_user_cannot_see_feedback_form(self):
        self.create_video('', False, timezone.now())
        self.client.login(username='user', password='passphrase')
        response = self.client.get(
            reverse('videos-by-filter', kwargs={'slug': 'test-0'}))

        self.assertNotContains(
            response,
            'Оставьте молитвенную записку, чтобы во время служения Церковь могла молиться за Вашу нужду.')

    def test_authorized_user_see_custom_feedback_text(self):
        text = 'Здесь вы можете оставить ваш вопрос'
        self.create_video(text, True)
        self.client.login(username='user', password='passphrase')
        response = self.client.get(
            reverse('videos-by-filter', kwargs={'slug': 'test-0'}))

        self.assertContains(response, text)

    def test_authorized_user_can_send_feedback_only_2_times_per_hour(self):
        self.create_video('', True)

        self.client.login(username='user', password='passphrase')
        text = 'тестовый запрос'
        for item in range(2):
            self.client.post(reverse(
                'videos-by-filter', kwargs={'slug': 'test-0'}), data={'description': text})

        response = self.client.post(reverse(
            'videos-by-filter', kwargs={'slug': 'test-0'}), data={'description': text})

        self.assertContains(
            response, 'Превышено количество сообщений в час. (Две записки в час).')

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
