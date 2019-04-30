from datetime import datetime, timedelta
import logging

from django.core import mail
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib.syndication.views import Feed
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models.functions import TruncMonth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template

from .models import NewsItem, Event, MailingLog, Subscriber
from articles.models import Article


logger = logging.getLogger('ECHB')


class NewsListView(ListView):
    model = NewsItem
    paginate_by = 7

    def _get_archive_months(self):
        time_delta = datetime.today() - timedelta(18*(365/12))
        dates = NewsItem.objects.values('publication_date').filter(publication_date__gte=time_delta).annotate(
            month=TruncMonth('publication_date')).distinct('month').order_by('-month')
        return dates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['archive_news'] = self._get_archive_months()

        return context

    def get_queryset(self):
        if 'month' in self.kwargs and 'year' in self.kwargs:
            return self.model.objects.filter(
                publication_date__month=self.kwargs['month'],
                publication_date__year=self.kwargs['year']).select_related('author')
        else:
            return self.model.objects.filter(publication_date__lt=datetime.now()).select_related('author').order_by('-publication_date')


class NewsDetailView(DetailView):
    model = NewsItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = NewsItem.objects.order_by('-publication_date')[:5]
        context['domain'] = get_current_site(self.request)
        return context


class LatestEntriesFeed(Feed):
    title = "Последние новости"
    link = "/news/latest/feed/"
    description = "Обновления новостей Харьковского объединения евангельских христиан-баптистов"

    def items(self):
        return NewsItem.objects.filter(publication_date__lt=datetime.now()).order_by('-publication_date')[:7]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description[:200] + '...' if len(item.description) > 200 else item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news-detail', args=[item.pk])


class EventDetailView(DetailView):
    model = Event


class SearchListView(ListView):
    model = NewsItem
    template_name = 'newsevents/search.html'
    context_object_name = 'results'
    paginate_by = 7

    def get_queryset(self):
        if 'query' in self.request.GET:
            query = self.request.GET['query']
            return NewsItem.objects.annotate(search=SearchVector('title', 'description')).filter(search=query)
        else:
            return NewsItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET['query']
        context['latest_news'] = NewsItem.objects.order_by('-publication_date')[:5]
        return context


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
