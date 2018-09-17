from django.test import TestCase
from django.test import Client
from django.urls import reverse
from decouple import config
from django.contrib.staticfiles.templatetags.staticfiles import static

from .forms import UploadZipForm
from .models import Author, Tag, Image

class ImageUploadTests(TestCase):
    def setUp(self):
        author = Author()
        author.first_name = 'George'
        author.last_name = 'Rondem'
        author.save()

        tag = Tag()
        tag.name = 'test'
        tag.save()
    
    def test_gallery_created(self):
        c = Client()
        response = c.post('/admin/login/', {'username': config('ADMIN_LOGIN'), 'password': config('ADMIN_PASSWORD')})

        change_url = '/admin/galleries/gallery/upload_zip/'
        author_id = Author.objects.all().first().id
        data = {
            'zip_file':'/static/media/galleries/test_gallery.zip',
            'title':'Test gallery',
            'date':'09.02.2018',
            'author': author_id
        }

        response = c.post(change_url, data)
        #self.assertIs(response.status_code, 200)
        #gallery = Gallery.objects.all().first()
        #self.assertEqual(gallery.title, 'Test gallery')
