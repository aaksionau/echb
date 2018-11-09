from datetime import datetime
import os
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase

from galleries.models import Author, Gallery, Image, Tag


class ImageUploadTests(TestCase):
    path_to_zip = os.path.join(settings.BASE_DIR, 'galleries', 'tests', 'test_gallery.zip')
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

    def test_gallery_created(self):
        self.client.login(username='admin', password='passphrase')

        author = Author.objects.all().first()
        tag = Tag.objects.all().first()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'Test gallery',
                'date': '09.02.2018',
                'author': author.pk,
                'tags': tag.id
            }
            self.client.post(self.change_url, data, follow=True)

        self.assertEqual(len(Gallery.objects.all()), 1)

    def test_after_uploading_zip_there_is_main_image(self):
        self.client.login(username='admin', password='passphrase')

        author = Author.objects.all().first()
        tag = Tag.objects.all().first()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'Test gallery',
                'date': '09.02.2018',
                'author': author.pk,
                'tags': tag.id
            }
            response = self.client.post(self.change_url, data, follow=True)
            self.assertEqual(response.status_code, 200)

        gallery = Gallery.objects.all().first()
        self.assertIsNotNone(gallery)
        self.assertTrue(gallery.main_image)

    def test_slug_already_exists(self):

        self.client.login(username='admin', password='passphrase')

        author = Author.objects.all().first()

        gallery = Gallery()
        gallery.title = "test"  # slug is formed out of title
        gallery.date = datetime.now()
        gallery.author = author
        gallery.save()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'test',
                'date': '09.02.2018',
                'author': author.pk
            }
            response = self.client.post(self.change_url, data, follow=True)
            self.assertContains(response, 'Галерея с таким названием уже существует')

    def test_add_images_to_existing_gallery(self):

        self.client.login(username='admin', password='passphrase')
        author = Author.objects.all().first()
        tag = Tag.objects.all().first()

        gallery = Gallery()
        gallery.title = "test"  # slug is formed out by slugifying title
        gallery.date = datetime.now()
        gallery.author = author
        gallery.save()

        gallery.tags.set([tag])
        gallery.save()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'gallery': gallery.pk
            }
            response = self.client.post(self.change_url, data, follow=True)
            self.assertContains(response, 'Фотографии были добавлены')

        self.assertEqual(len(Gallery.objects.all()), 1)

        count = Image.objects.filter(gallery_id=gallery.id).count()
        self.assertGreater(count, 0)

    def test_new_gallery_missing_author(self):
        self.client.login(username='admin', password='passphrase')

        tag = Tag.objects.all().first()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'test',
                'date': '09.02.2018',
                'tags': tag.id}
            response = self.client.post(self.change_url, data, follow=True)
            self.assertContains(response, 'Для новой галереи поля date, author, tags - обязательны')

    def test_new_gallery_missing_date(self):
        self.client.login(username='admin', password='passphrase')

        tag = Tag.objects.all().first()
        author = Author.objects.all().first()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'test',
                'author': author.pk,
                'tags': tag.id}

            response = self.client.post(self.change_url, data, follow=True)
            self.assertContains(response, 'Для новой галереи поля date, author, tags - обязательны')

    def test_new_gallery_missing_tags(self):
        self.client.login(username='admin', password='passphrase')

        author = Author.objects.all().first()

        with open(self.path_to_zip, 'rb') as fp:
            data = {
                'zip_file': fp,
                'title': 'test',
                'author': author.pk,
                'date': '09.02.2018'}

            response = self.client.post(self.change_url, data, follow=True)
            self.assertContains(response, 'Для новой галереи поля date, author, tags - обязательны')

    @patch('zipfile.ZipFile')
    def test_zip_file_size_greater_than_10Mb(self, mock_zipfile):

        self.client.login(username='admin', password='passphrase')

        # https://docs.python.org/3/library/zipfile.html
        # Mocking that our file is a Zip file

        mock_zipfile.return_value = MagicMock(is_zipfile=True)
        # set a size to 11Mb
        mock_zipfile.return_value.fp.size = 1024*1024*11
        # return None which indicates that zip file doesnt contain any bad files
        mock_zipfile.return_value.testzip.return_value = None
        zipfile = mock_zipfile('file.zip')

        author = Author.objects.all().first()
        tag = Tag.objects.all().first()
        data = {
            'zip_file': zipfile,
            'title': 'test',
            'author': author.pk,
            'date': '09.02.2018',
            'tags': tag.id}

        response = self.client.post(self.change_url, data, follow=True)
        self.assertContains(response, 'Размер файла превышает 10 Мб')
