
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..views import SignUpFormView
from ..forms import SignUpForm


from pages.models import Page


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        add_pages()
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@test.ru',
            'password1': '#4erdfcV1234',
            'password2': '#4erdfcV1234'
        }
        self.response = self.client.post(url, data)
        self.create_video_page()
        self.videos_url = reverse('online')

    def create_video_page(self):
        about = Page.objects.create(title='about-us', slug='about-us')
        Page.objects.create(title='online', slug='online', parent=about)

    def test_redirection(self):
        self.assertRedirects(self.response, self.videos_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.videos_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class SignUpTests(TestCase):
    def setUp(self):
        add_pages()
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func.view_class, SignUpFormView)

    def test_signup_form_on_the_page(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


def add_pages():

    for item in ['accounts']:
        Page.objects.create(
            title=item, slug=item.lower(), visible_in_menu=True
        )

    accounts = Page.objects.get(slug='accounts')

    for item in ['login', 'signup', ]:
        Page.objects.create(title=item, slug=item, parent=accounts)
