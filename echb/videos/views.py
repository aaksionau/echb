from datetime import timedelta, datetime

from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.models import User

from django.views.generic import DetailView, ListView
from django.views.generic.edit import ModelFormMixin

from .models import Video, PrayerRequest, VideoCategory
from .forms import PrayerRequestForm

MAX_MESSAGES_PER_HOUR = 2


class VideoDetailView(ModelFormMixin, DetailView):
    model = Video
    form_class = PrayerRequestForm
    success_url = '/about-us/online/thankyou/'

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        self.object = self.get_object()
        form = PrayerRequestForm(self.request.POST)
        user = User.objects.get(username=self.request.user)
        if form.is_valid() and self.validate_max_messages(user):
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def validate_max_messages(self, user):

        time_delta = datetime.today() - timedelta(hours=1)
        messages_count = PrayerRequest.objects.filter(created__gte=time_delta, user=user).count()
        if messages_count >= MAX_MESSAGES_PER_HOUR:
            return False

        return True


class CurrentVideosListView(ListView):
    template_name = 'videos/current_videos.html'
    model = VideoCategory

    def get_video_categories(self):
        time_delta = datetime.today() - timedelta(days=7)
        return (Video
                .objects
                .filter(date__gte=time_delta)
                .select_related('category')
                .values_list('category__slug'))

    def get_queryset(self):
        queryset = VideoCategory.objects.filter(slug__in=self.get_video_categories())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CurrentVideosListView, self).get_context_data(**kwargs)

        time_delta = datetime.today() - timedelta(days=7)
        videos = {}
        for category in self.get_video_categories():
            category_slug = category[0]
            videos[category_slug] = Video.objects.filter(category__slug=category_slug).filter(date__gte=time_delta)

        context['video_list'] = videos
        return context


class VideoListView(ListView):
    template_name = 'videos/videos.html'
    model = Video

    def get_queryset(self):
        queryset = Video.objects.filter(interesting_event=True).select_related('category').order_by('-date')
        return queryset
