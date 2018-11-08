import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Author, Tag, Gallery, Image


class ImageUploadTests(TestCase):
    change_url = '/admin/galleries/gallery/upload_zip/'

    def setUp(self):

        admin = User(username='admin', is_staff=True)
        admin.set_password('passphrase')
        admin.is_superuser = True
        admin.save()

        author = Author()
        author.first_name = 'George'
        author.last_name = 'Ronde'
        author.save()

        tag = Tag()
        tag.name = 'test'
        tag.save()

        self.client = Client()

    # def test_gallery_created(self):
    #     self.client.login(username='admin', password='passphrase')

    #     author = Author.objects.all().first()

    #     with open('./static/media/galleries/test_gallery.zip', 'rb') as fp:
    #         data = {
    #             'zip_file': fp,
    #             'title': 'Test gallery',
    #             'date': '09.02.2018',
    #             'author': author.pk
    #         }
    #         response = self.client.post(self.change_url, data, follow=True)
    #         self.assertEqual(response.status_code, 200)

    #         self.assertEqual(len(Gallery.objects.all()), 1)

    # def test_after_uploading_zip_there_is_main_image(self):
    #     self.client.login(username='admin', password='passphrase')

    #     author = Author.objects.all().first()

    #     with open('./static/media/galleries/test_gallery.zip', 'rb') as fp:
    #         data = {
    #             'zip_file': fp,
    #             'title': 'Test gallery',
    #             'date': '09.02.2018',
    #             'author': author.pk
    #         }
    #         response = self.client.post(self.change_url, data, follow=True)
    #         self.assertEqual(response.status_code, 200)

    ##     gallery = Gallery.objects.all().first()
    #     self.assertTrue(gallery.main_image)

    # def test_slug_already_exists(self):

    #     self.client.login(username='admin', password='passphrase')

    #     author = Author.objects.all().first()

    #     gallery = Gallery()
    #     gallery.title = "test"  # slug is formed out of title
    #     gallery.date = datetime.datetime.now()
    #     gallery.author = author
    #     gallery.save()

    #     with open('./static/media/galleries/test_gallery.zip', 'rb') as fp:
    #         data = {
    #             'zip_file': fp,
    #             'title': 'test',
    #             'date': '09.02.2018',
    #             'author': author.pk
    #         }
    #         response = self.client.post(self.change_url, data, follow=True)
    #         self.assertContains(response, 'Галерея с таким названием уже существует')

    # def test_add_images_to_existing_gallery(self):

    #     self.client.login(username='admin', password='passphrase')
    #     author = Author.objects.all().first()

    #     gallery = Gallery()
    #     gallery.title = "test"  # slug is formed out of title
    #     gallery.date = datetime.datetime.now()
    #     gallery.author = author
    #     gallery.save()

    #     with open('./static/media/galleries/test_gallery.zip', 'rb') as fp:
    #         data = {
    #             'zip_file': fp,
    #             'date': '09.02.2018',
    #             'gallery': gallery.pk
    #         }
    #         response = self.client.post(self.change_url, data, follow=True)
    #         self.assertContains(response, 'Фотографии были добавлены')

    #     self.assertEqual(len(Gallery.objects.all()), 1)

    #     count = Image.objects.filter(gallery_id=gallery.id).count()
    #     self.assertGreater(count, 0)
