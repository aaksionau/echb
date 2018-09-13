from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertAlmostEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@ukr.net'
        User.objects.create_user(username='john', email=email, password="@3wesdxC")
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email':email})

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email':'alex@ukr.net'})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_send_password_reset_email(self):
        self.assertEqual(0, len(mail.outbox))