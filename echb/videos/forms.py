from django import forms
from django.forms import ModelForm

from .models import PrayerRequest


class PrayerRequestForm(ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['description']

        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Введите ваше сообщение', 'class': 'form__text', 'rows': 5}),
        }
        labels = {
            'description': ''
        }
