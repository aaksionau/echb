import logging
import os
from datetime import datetime, timedelta

import requests
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import TemplateView, View

from accounts.forms import PrayerRequestForm
from articles.models import Article
from galleries.models import Gallery
from newsevents.models import Event, NewsItem

from .forms import FeedbackForm, SubscriberForm
from .models import MailingLog, Page, Subscriber, Video

logger = logging.getLogger('ECHB')


class HomePageView(View):
    def get(self, request):
        context = self._get_context_data()
        return render(request, 'pages/home.html', context)

    def post(self, request):
        form = SubscriberForm(request.POST)
        context = self._get_context_data()

        captcha_is_valid = check_captcha(request)

        if form.is_valid() and captcha_is_valid:
            subscriber = form.save()
            domain = form.get_domain(request)
            form.send_mail(subscriber, domain)

            context['success_subscriber'] = True
            return render(request, 'pages/subscription_thankyou.html')
        else:
            context['errors'] = form.errors['email']
            return render(request, 'pages/home.html', context)

    def _get_context_data(self):
        page = Page.objects.get(slug='home')
        news = NewsItem.objects.all().order_by('-publication_date')[:6]
        articles = Article.objects.all().order_by('-date').select_related('author').select_related('category')[:6]
        events = Event.objects.filter(date__gt=datetime.now()).order_by('date')[:6]
        photos = Gallery.objects.all().order_by('-date')[:4]
        form = SubscriberForm()
        context = {
            'page': page,
            'news': news,
            'articles': articles,
            'events': events,
            'photos': photos,
            'form': form
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
            'video': Video.objects
            .filter(date__gte=time_delta)
            .filter(category__slug=self.kwargs['slug'])
            .select_related('category').order_by('-date').first(),
            'categories': Video.objects.filter(date__gte=time_delta).select_related('category')
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
            return redirect('video-detail-thankyou', slug=slug)
        else:
            messages.info(request, 'Ваше сообщение слишком длинное. Максимум 250 символов.')
            return render(request, 'pages/video_detail.html', context)


class CurrentVideosListView(ListView):
    template_name = 'pages/current_videos.html'
    model = Video

    def get_queryset(self):
        time_delta = datetime.today() - timedelta(days=7)
        queryset = Video.objects.filter(date__gte=time_delta).select_related('category')
        return queryset


class VideoListView(ListView):
    template_name = 'pages/videos.html'
    model = Video

    def get_queryset(self):
        queryset = Video.objects.filter(interesting_event=True).select_related('category').order_by('-date')
        return queryset


class ContactsFormView(FormView):
    template_name = 'pages/contacts.html'
    success_url = '/contacts/thankyou/'
    form_class = FeedbackForm

    def form_valid(self, form, **kwargs):
        captcha_is_valid = check_captcha(self.request)

        if captcha_is_valid:
            form.send_email()
            form.save()
            return super().form_valid(form)
        else:
            return redirect('contacts')


class ContactsThankYouView(TemplateView):
    template_name = 'pages/thankyou.html'


class ActivateSubscriber(View):
    def get(self, request, uuid):
        subscriber = Subscriber.objects.filter(uuid=uuid).first()

        if subscriber:
            subscriber.activated = True
            subscriber.save()

            send_mail(request, [subscriber.email, ])

            return redirect('subscriber-activated')
        return redirect('home')


class SendLetterToSubscribers(View):
    def get(self, request):
        last_month = datetime.now() - timedelta(days=30)
        already_sent = MailingLog.objects.filter(date__gte=last_month).filter(date__lte=datetime.now()).first()

        if already_sent is not None:
            return HttpResponse(f'Letters were sent earlier: {already_sent.date.strftime("%d/%m/%y")}',
                                content_type="text/plain")

        subscribers = Subscriber.objects.filter(activated=True)

        emails = [subscriber.email for subscriber in subscribers]
        send_mail(request, emails)
        return HttpResponse(f'Letters were successfuly sent: {timezone.now().strftime("%d/%m/%y")}',
                            content_type="text/plain")


def get_context_for_letter(request):
    time_delta_past = datetime.today() - timedelta(days=30)
    time_delta_future = datetime.today() + timedelta(days=30)
    news = NewsItem.objects.filter(publication_date__gte=time_delta_past).filter(
        publication_date__lt=datetime.today()).filter(published=True)
    events = Event.objects.filter(date__gt=datetime.today()).filter(date__lt=time_delta_future)
    articles = Article.objects.filter(date__gte=time_delta_past).filter(
        date__lt=datetime.today()).select_related('category').select_related('author')
    domain = get_domain(request)
    context = {
        'news': news,
        'events': events,
        'articles': articles,
        'domain': domain
    }
    return context


class Letter(View):
    def get(self, request):
        context = get_context_for_letter(request)
        return render(request, 'newsevents/letter.html', context)


def send_mail(request, emails):
    mailing_log = MailingLog()
    mailing_log.save()

    context = get_context_for_letter(request)
    message = get_template('newsevents/letter.html').render(context)

    emails_for_log = emails[:]  # to change array if there is any error with email

    for address in emails:
        try:
            with mail.get_connection() as connection:
                email = mail.EmailMessage(
                    subject='Последние новости с сайта ecb.kh.ua',
                    body=message,
                    to=(address,),
                    connection=connection
                )
                email.content_subtype = 'html'
                email.send()
        except Exception as e:
            emails_for_log.pop(address, None)
            logger.error(f'Errors on newsletter sending: {e.args}')

    mailing_log_finished = MailingLog.objects.filter(pk=mailing_log.id).first()
    mailing_log_finished.message = message
    mailing_log_finished.finished = timezone.now()
    mailing_log_finished.emails = emails_for_log
    mailing_log_finished.save()

    return mailing_log_finished


def get_domain(request):
    current_site = get_current_site(request)
    return f'{request.scheme}://{current_site.domain}'


def check_captcha(request):
    captcha = request.POST.get('g-recaptcha-response')
    response = requests.post("https://www.google.com/recaptcha/api/siteverify",
                             data={'secret': '6LfamGAUAAAAAEnS0-AF5p_EVmAFriMZqkkll-HM', 'response': captcha})

    debug_mode = bool(os.environ.get("DEBUG", False))

    return debug_mode if debug_mode else response.json()['success']


def handler404(request, exception, template_name='pages/404.html'):
    response = render_to_response('pages/404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('pages/500.html')
    response.status_code = 500
    return response
