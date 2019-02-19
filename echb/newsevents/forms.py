from django import forms
from django.forms import ModelForm
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.template.loader import get_template

from .models import Subscriber


class SearchForm(forms.Form):
    query = forms.CharField()


class SubscriberForm(ModelForm):
    def get_domain(self, request):
        current_site = get_current_site(request)
        return current_site.domain

    def send_mail(self, subscriber, domain):
        email = self.cleaned_data['email']
        message = get_template(
            'pages/subscriber_activation_letter.html').render({'subscriber': subscriber, 'domain': domain})
        with mail.get_connection() as connection:
            email = mail.EmailMessage(
                subject='Подтверждение о подписке на новости',
                body=message,
                to=(email,),
                connection=connection
            )
            email.content_subtype = 'html'
            email.send()

    class Meta:
        model = Subscriber
        fields = ['email']
