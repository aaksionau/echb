from datetime import datetime, timedelta

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.urls import resolve
from django.template import RequestContext

from .models import Page, Feedback, Video, VideoCategory, Subscriber
from accounts.models import PrayerRequest
from newsevents.models import NewsItem, Event
from articles.models import Article
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
        form = SubscriberForm()
        context = {
            'page': page,
            'news': news,
            'articles': articles,
            'events': events,
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
    category = 'preobrazhenie'
    def get_context_data(self):
        context = {
            'video': Video.objects.filter(category__slug = self.category).select_related('category').order_by('date').first(),
            'categories': VideoCategory.objects.all()
        }
        return context
    
    def get(self, request):
        context = self.get_context_data()
        context['form'] = PrayerRequestForm()
        return render(request, 'pages/video_preobrazhenie.html', context)

    def post(self, request):
        form = PrayerRequestForm(request.POST)
        context = self.get_context_data()

        if not form.prayer_request_count_allowed(request.user):
            context['message'] ='Превышено количество сообщений в час. (Две записки в час).'
            return render(request, 'pages/video_preobrazhenie.html', context)

        if form.is_valid():
            prayer_request = form.save(commit=False)
            prayer_request.user = request.user
            prayer_request.save()
            return redirect('video-preobrazhenie-thankyou')
        else:
            return redirect('video-preobrazhenie')

class VideoListView(ListView):
    template_name = 'pages/videos.html'
    model = Video
  
    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['categories'] = VideoCategory.objects.all()
        return context
    
    def get_queryset(self):
        queryset = Video.objects.filter(category__slug = self.kwargs['category']).select_related('category').order_by('-date')
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
        subscriber = Subscriber.objects.get(uuid=uuid)

        if subscriber:
            subscriber.activated = True
            subscriber.save()

            return redirect('subscriber-activated')
        redirect('home')

def handler404(request, exception, template_name='pages/404.html'):
    response = render_to_response('pages/404.html')
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('pages/500.html')
    response.status_code = 500
    return response