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

    # User can see categories

    def test_user_can_see_links_to_videos(self):
        self.create_video('', True)
        self.create_video('', True)
        response = self.client.get(reverse('online'))

        self.assertContains(response, 'class="video-cat__video-link"', count=2)

# User can see several links under categories if there videos are 7 days old
# User can send a prayer request
# User cannot send prayer request 3 and more times
# User cannot send request with message longer then 250 symbols
# Unauthorised user can not send a request
# if there are no available videos - show text and also show section with interesting videos

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

        return video.pk
