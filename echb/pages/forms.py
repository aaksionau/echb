from django.forms import ModelForm
from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template

from .models import Feedback, Subscriber

class FeedbackForm(ModelForm):
    def _send_message(self, subject, message, recipients):
        with mail.get_connection() as connection:
            email = mail.EmailMessage(
                subject=subject,
                body=message,
                to=recipients,
                connection=connection
            )
            email.content_subtype = 'html'
            email.send()

    def send_email(self):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        cc_myself = self.cleaned_data['cc_myself']

        recipients = ['cbc.ooc.kh@gmail.com','valeryj82@gmail.com']
        self._send_message(subject, message, recipients)
        if cc_myself:
            recipients = [email]
            subject = 'Копия вашего сообщения с сайта Харьков для Христа: ' + subject
            self._send_message(subject, message, recipients)
            
    class Meta:
        model = Feedback
        fields = ['name','email', 'subject','message', 'cc_myself']
        labels = {
            'name': 'Ваше имя',
            'email': 'Ваш email',
            'cc_myself': 'Отправить копию сообщения мне',
            'subject': 'Тема сообщения',
            'message': 'Ваше сообщение'
        }

class SubscriberForm(ModelForm):
    def get_domain(self, request):
        current_site = get_current_site(request)
        return current_site.domain

    def send_mail(self, subscriber, domain):
        email = self.cleaned_data['email']
        message = get_template('pages/subscriber_activation_letter.html').render({'subscriber':subscriber,'domain':domain})
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