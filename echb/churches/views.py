import logging

from django.core import serializers
from django.shortcuts import HttpResponse, render

from .models import Church, Region

logger = logging.getLogger('ECHB')


def find_church(request):
    return render(request, 'churches/churches.html')


def get_churches(request):
    queryset = Church.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('churches = ' + data, content_type='text/javascript')


def get_regions(request):
    queryset = Region.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('regions = ' + data, content_type='text/javascript')
