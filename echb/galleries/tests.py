from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Author, Tag, Gallery


class ImageUploadTests(TestCase):
    def setUp(self):

        admin = User(username='admin', is_staff=True)
        admin.set_password('passphrase')
        admin.is_superuser = True
        admin.save()

        author = Author()
        author.first_name = 'George'
        author.last_name = 'Rondem'
        author.save()

        tag = Tag()
        tag.name = 'test'
        tag.save()

        self.client = Client()

    def test_gallery_created(self):
        self.client.login(username='admin', password='passphrase')

        change_url = '/admin/galleries/gallery/upload_zip/'
        author = Author.objects.all().first()

        with open('./static/media/galleries/test_gallery.zip', 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'Test gallery',
                'date': '09.02.2018',
                'author': author.pk
            }
            response = self.client.post(change_url, data, follow=True)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(len(Gallery.objects.all()), 1)
