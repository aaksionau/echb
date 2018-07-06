import json, os
from django.shortcuts import render
from django.db.models.functions import TruncYear
from django.views.generic import ListView, DetailView
from datetime import datetime, timedelta
import re
import csv

from .models import *


class ExtraContext(object):
    extra_context = {}

    def _get_archive_months(self):
        time_delta = datetime.today() - timedelta(72*(365/12))
        dates = Gallery.objects.values('date').filter(date__gte=time_delta).annotate(year=TruncYear('date')).distinct('year').order_by('-year')
        return dates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['archive_galleries'] = self._get_archive_months()
        context['authors'] = Author.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class GalleriesListView(ExtraContext, ListView):
    model = Gallery
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.select_related('author')

class GalleriesFilterByTagListView(ExtraContext, ListView):
    model = Gallery
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(tags__in=[self.kwargs['tag']]).select_related('author')

class GalleriesFilterByAuthorListView(ExtraContext, ListView):
    model = Gallery
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(author__id=self.kwargs['author']).select_related('author')

class GalleriesArchiveListView(ExtraContext, ListView):
    model = Gallery
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(date__year=self.kwargs['year']).select_related('author')

class GalleryDetailView(DetailView):
    model = Gallery

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['latest_galleries'] = Gallery.objects.order_by('-date')[:6]
        data['images'] = Image.objects.filter(gallery_id = Gallery.objects.get(slug = self.kwargs['slug']).id)
        return data