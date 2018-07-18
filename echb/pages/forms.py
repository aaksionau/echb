from django.forms import ModelForm
from django.core import mail

from .models import Feedback, PrayerRequest, Subscriber

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

        recipients = ['alexei.aksenov@gmail.com']
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


class PrayerRequestForm(ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['description']

class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']