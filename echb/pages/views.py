from datetime import datetime, timedelta

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.urls import resolve
from django.template import RequestContext

from .models import Page, Ministry, Feedback, Video, VideoCategory, PrayerRequest, Subscriber
from newsevents.models import NewsItem, Event
from articles.models import Article
from .forms import FeedbackForm, PrayerRequestForm, SubscriberForm

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
            return render(request, 'pages/home.html', context)
        else:
            context['errors'] = form.errors
            return render(request, 'pages/home.html', context)

    def _get_context_data(self):
        page = Page.objects.get(slug='home')
        news = NewsItem.objects.all().order_by('-publication_date')[:6]
        articles = Article.objects.all().order_by('-date').select_related('author').select_related('category')[:6]
        ministries = Ministry.objects.all()
        events = Event.objects.all().order_by('date')[:3]
        form = SubscriberForm()
        context = {
            'page': page,
            'news': news,
            'articles': articles,
            'events': events,
            'ministries': ministries,
            'form':form
        }
        return context

def get_prayer_requests():
    date_delta = datetime.now() -  timedelta(days=6)
    prayer_requests_all = PrayerRequest.objects.filter(created__gte = date_delta).select_related('user').order_by('created')

    return date_delta, prayer_requests_all

def prayerrequests(request):
    date_delta, prayer_requests_all = get_prayer_requests()
    users = User.objects.values('id','username')
    prayers = []
    for item in prayer_requests_all.values('user_id', 'description', 'created', 'user'):
        username = [user['username'] for user in users if user['id'] == item['user_id']][0]
        prayer = Prayer(str(item['created']), username, item['description'])
        prayers.append(prayer)

    data = simplejson.dumps([p.__dict__ for p in prayers])
    return HttpResponse(data, content_type='application/json')

class ExtraContext(object):
    
    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['right_menu_ministries'] = Ministry.objects.all()
        return context

class PageDetailView(DetailView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['right_menu_pages'] = Page.objects.filter(parent__slug='about-us').order_by('order')
        context['church_history_pages'] = Page.objects.filter(parent__slug='churches-history')
        return context

class MinistryDetailView(ExtraContext, DetailView):
    model = Ministry

class MinistryListView(ExtraContext, ListView):
    model = Ministry

def videos(request, category='preobrazhenie'):
    
        videos = None
        categories = VideoCategory.objects.all()
        message = ''
        if category == 'preobrazhenie':
            if request.method == 'POST':
                form = PrayerRequestForm(request.POST)
                if form.is_valid():
                    prayer_request = form.save(commit=False)
                    prayer_request.user = request.user
                    prayer_request.save()
                    message = 'О вашей нужде помолятся в течении богослужения.'

            videos = Video.objects.filter(category__slug = category).select_related('category').order_by('date').first()
            form = PrayerRequestForm()
            return render(request, 'pages/video_preobrazhenie.html', {'video':videos, 'categories':categories, 'form':form, 'message':message })
        else:
            videos = Video.objects.filter(category__slug = category).select_related('category').order_by('date')
            return render(request, 'pages/videos.html', {'videos':videos, 'categories':categories})

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

        return redirect('home')

def handler404(request, exception, template_name='pages/404.html'):
    response = render_to_response('pages/404.html')
    response.status_code = 404
    return response

def handler500(request, exception, template_name='pages/500.html'):
    response = render_to_response('pages/500.html')
    response.status_code = 500
    return response



class Prayer:
    def __init__(self, date_created, username, description):
        self.date_created = date_created
        self.username = username
        self.description = description