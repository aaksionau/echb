from django.forms import ModelForm

from .models import Feedback, PrayerRequest

class FeedbackForm(ModelForm):
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