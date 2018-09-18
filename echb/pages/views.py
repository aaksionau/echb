from datetime import datetime, timedelta

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.urls import resolve
from django.template import RequestContext
from django.contrib import messages

from .models import Page, Feedback, Video, VideoCategory, Subscriber
from accounts.models import PrayerRequest
from newsevents.models import NewsItem, Event
from articles.models import Article
from galleries.models import Gallery
from .forms import FeedbackForm, SubscriberForm
from accounts.forms import PrayerRequestForm

class HomePageView(View):
    def get(self, request):
        context = self._get_context_data()
        return render(request, 'pages/home.html', context)

    def post(self, request):
        form = SubscriberForm(request.POST)
        context = self._get_context_data()
        if form.is_valid():
            subscriber = form.save()
            domain = form.get_domain(request)
            form.send_mail(subscriber, domain)

            context['success_subscriber'] = True
            return render(request, 'pages/subscription_thankyou.html')
        else:
            context['errors'] = form.errors
            return render(request, 'pages/home.html', context)

    def _get_context_data(self):
        page = Page.objects.get(slug='home')
        news = NewsItem.objects.all().order_by('-publication_date')[:6]
        articles = Article.objects.all().order_by('-date').select_related('author').select_related('category')[:6]
        events = Event.objects.all().order_by('date')[:3]
        photos = Gallery.objects.all().order_by('-date')[:4]
        form = SubscriberForm()
        context = {
            'page': page,
            'news': news,
            'articles': articles,
            'events': events,
            'photos':photos,
            'form':form
        }
        return context

class PageDetailView(DetailView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['right_menu_pages'] = Page.objects.filter(parent__slug='about-us').order_by('order')
        context['church_history_pages'] = Page.objects.filter(parent__slug='churches-history')
        return context


class VideoDetailView(View):
    def get_context_data(self):
        time_delta = datetime.today() - timedelta(days=7)
        context = {
            'video': Video.objects.filter(date__gte = time_delta).filter(category__slug = self.kwargs['slug']).select_related('category').order_by('-date').first(),
            'categories': Video.objects.filter(date__gte = time_delta).select_related('category')
        }
        return context
    
    def get(self, request, slug):
        context = self.get_context_data()
        context['form'] = PrayerRequestForm()
        return render(request, 'pages/video_detail.html', context)

    def post(self, request, slug):
        form = PrayerRequestForm(request.POST)
        context = self.get_context_data()

        if not form.prayer_request_count_allowed(request.user):
            messages.info(request, 'Превышено количество сообщений в час. (Две записки в час).')
            return render(request, 'pages/video_detail.html', context)

        if form.is_valid():
            prayer_request = form.save(commit=False)
            prayer_request.user = request.user
            prayer_request.save()
            return redirect('video-detail-thankyou',slug=slug)
        else:
            messages.info(request, 'Ваше сообщение слишком длинное. Максимум 250 символов.')
            return render(request, 'pages/video_detail.html', context)

class CurrentVideosListView(ListView):
    template_name = 'pages/current_videos.html'
    model = Video
    

    def get_queryset(self):
        time_delta = datetime.today() - timedelta(days=7)
        queryset = Video.objects.filter(date__gte = time_delta).select_related('category')
        return queryset
    

class VideoListView(ListView):
    template_name = 'pages/videos.html'
    model = Video
  
    def get_queryset(self):
        queryset = Video.objects.filter(interesting_event = True).select_related('category').order_by('-date')
        return queryset

class ContactsFormView(FormView):
    template_name = 'pages/contacts.html'
    success_url = '/contacts/thankyou/'
    form_class = FeedbackForm

    def form_valid(self, form):
        form.send_email()
        form.save()
        return super().form_valid(form)

class ContactsThankYouView(TemplateView):
    template_name = 'pages/thankyou.html'

class ActivateSubscriber(View):
    def get(self, request, uuid):
        subscriber = Subscriber.objects.filter(uuid=uuid).first()

        if subscriber:
            subscriber.activated = True
            subscriber.save()

            return redirect('subscriber-activated')
        return redirect('home')

def handler404(request, exception, template_name='pages/404.html'):
    response = render_to_response('pages/404.html')
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('pages/500.html')
    response.status_code = 500
    return response