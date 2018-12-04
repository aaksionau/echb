from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import PrayerRequest


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Ваш email', 'class': 'form__text'}))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form__text'}),
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя для сайта', 'class': 'form__text'})
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form__text',
                'placeholder': 'Введите пароль (как минимум 8 символов, состоящий из букв и цифр)'
            }
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form__text', 'placeholder': 'Повторите пароль'})


class PrayerRequestForm(ModelForm):

    def prayer_request_count_allowed(self, user):
        time_delta = datetime.today() - timedelta(hours=1)
        requests_count = PrayerRequest.objects.filter(created__gte=time_delta, user_id=user.id).count()
        return True if requests_count < 2 else False

    class Meta:
        model = PrayerRequest
        fields = ['description']
