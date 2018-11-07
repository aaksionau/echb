from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import PrayerRequest


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')


class PrayerRequestForm(ModelForm):

    def prayer_request_count_allowed(self, user):
        time_delta = datetime.today() - timedelta(hours=1)
        requests_count = PrayerRequest.objects.filter(created__gte=time_delta, user_id=user.id).count()
        return True if requests_count < 2 else False

    class Meta:
        model = PrayerRequest
        fields = ['description']
