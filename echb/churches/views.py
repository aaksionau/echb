import logging

from django.core import serializers
from django.shortcuts import HttpResponse, render

from .models import Church, Region

logger = logging.getLogger('ECHB')


def find_church(request):
    return render(request, 'churches/churches.html')


def string_to_model(argument):
    switcher = {
        "churches": Church,
        "regions": Region
    }
    return switcher.get(argument, None)


def get_data(request, type):
    type = string_to_model(type)
    if type:
        queryset = type.objects.all()
        data = serializers.serialize('json', queryset, ensure_ascii=False)
        return HttpResponse(data, content_type='json/javascript')
