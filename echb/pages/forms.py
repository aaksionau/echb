from django.forms import ModelForm
from django.core import mail
from django import forms

from .models import Feedback


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

        message_to_admin = f'Сообщение от {name}: {message}'

        recipients = ['cbc.ooc.kh@gmail.com', 'valeryj82@gmail.com']
        self._send_message(subject, message_to_admin, recipients)
        if cc_myself:
            recipients = [email]
            subject = 'Копия вашего сообщения с сайта Харьков для Христа: ' + subject
            self._send_message(subject, message, recipients)

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message', 'cc_myself']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form__text'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваше email', 'class': 'form__text'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Тема сообщения', 'class': 'form__text'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Ваше сообщение', 'class': 'form__text'}),
        }
        labels = {
            'cc_myself': 'Отправить копию сообщения мне'
        }
