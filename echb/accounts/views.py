from datetime import datetime, timedelta

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render
from django.views.generic.edit import FormView

from pages.models import OldUser, PrayerRequest
from .forms import SignUpForm

class SignUpFormView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/online/'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super(SignUpFormView, self).form_valid(form)

class LoginUser(LoginView):
    template_name = 'accounts/login.html'

class PrayerRequestsView(LoginRequiredMixin, ListView):
    model = PrayerRequest
    context_object_name = 'prayer_requests'
    template_name = 'accounts/prayerrequest_list.html'

    def get_prayer_requests(self):
        date_delta = datetime.now() -  timedelta(days=6)
        prayer_requests_all = PrayerRequest.objects.filter(created__gte = date_delta).select_related('user').order_by('created')

        return date_delta, prayer_requests_all

    def get_context_data(self, **kwargs):
        context = super(PrayerRequestsView, self).get_context_data(**kwargs)
        date_delta, prayer_requests_all = self.get_prayer_requests()
        context['last_video_date'] = date_delta
        context['prayer_requests_all'] = prayer_requests_all

        return context

    def get_queryset(self):
        queryset = super(PrayerRequestsView, self).get_queryset()
        queryset = PrayerRequest.objects.filter(user=self.request.user)
        return queryset

