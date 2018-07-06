from datetime import datetime, timedelta, date

from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.db.models.functions import TruncMonth
from django.template import RequestContext
from .models import NewsItem, Author, Event
from helpers.utils import BreadCrumLink

class NewsListView(ListView):
    model = NewsItem
    paginate_by = 7

    def _get_archive_months(self):
        time_delta = datetime.today() - timedelta(18*(365/12))
        dates = NewsItem.objects.values('publication_date').filter(publication_date__gte=time_delta).annotate(month=TruncMonth('publication_date')).distinct('month').order_by('-month')
        return dates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['archive_news'] = self._get_archive_months()

        return context
    
    def get_queryset(self):
        if 'month' in self.kwargs and 'year' in self.kwargs:
            return self.model.objects.filter(publication_date__month=self.kwargs['month'], publication_date__year=self.kwargs['year']).select_related('author')
        else:
            return self.model.objects.select_related('author').order_by('-publication_date')

class NewsDetailView(DetailView):
    model = NewsItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = NewsItem.objects.order_by('-publication_date')[:5]
        return context

class LatestEntriesFeed(Feed):
    title = "Последние новости"
    link = "/news/latest/feed/"
    description = "Обновления новостей Харьковского объединения евангельских христиан-баптистов"

    def items(self):
        return NewsItem.objects.order_by('-publication_date')[:7]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description[:200] + '...' if len(item.description) > 200 else item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news-detail', args=[item.pk])

class EventDetailView(DetailView):
    model = Event
