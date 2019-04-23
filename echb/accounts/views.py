from datetime import timedelta

from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView

from videos.models import Video

from .forms import SignUpForm
from videos.models import PrayerRequest


class SignUpFormView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/about-us/online/'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super(SignUpFormView, self).form_valid(form)


class LoginUser(LoginView):
    template_name = 'accounts/login.html'


class ProfileUserFormView(UpdateView):
    template_name = 'accounts/profile.html'
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = '/accounts/profile/success/'


class MyPrayerRequestListView(ListView):
    model = PrayerRequest
    context_object_name = 'my_prayer_requests'
    template_name = 'accounts/my_prayer_requests.html'

    def get_queryset(self):
        queryset = super(MyPrayerRequestListView, self).get_queryset()
        queryset = PrayerRequest.objects.filter(
            user=self.request.user).select_related('user')
        return queryset


class PrayerRequestsView(LoginRequiredMixin, ListView):
    model = PrayerRequest
    context_object_name = 'prayer_requests'
    template_name = 'accounts/prayerrequest_list.html'

    def get_prayer_requests(self):
        date_delta = timezone.now() - timedelta(days=6)
        prayer_requests_all = PrayerRequest.objects.filter(
            created__gte=date_delta).select_related('user').order_by('created')

        return date_delta, prayer_requests_all

    def get_context_data(self, **kwargs):
        context = super(PrayerRequestsView, self).get_context_data(**kwargs)
        date_delta, prayer_requests_all = self.get_prayer_requests()
        context['last_video_date'] = date_delta
        context['prayer_requests_all'] = prayer_requests_all
        context['video'] = Video.objects.all().select_related(
            'category').order_by('-date').first()

        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = self.get_context_data()["prayer_requests_all"].values(
                'user', 'description', 'created', 'user__first_name')
            return JsonResponse(list(data), safe=False)
        else:
            return ListView.render_to_response(self, context)
