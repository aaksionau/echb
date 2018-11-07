import json
import logging
import urllib.request
from urllib.parse import quote

from django.core import serializers
from django.shortcuts import HttpResponse, render

from .models import Church, Region

logger = logging.getLogger('ECHB')


def find_church(request):
    return render(request, 'churches/churches.html')


google_key = 'AIzaSyAP8zWTk8oq_9o_OXwSWvkBhZ65163UXhA'
google_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'


def geolocation(request):
    churches = Church.objects.all()

    for church in churches:
        address = quote(church.region.name + ' ' + church.address)

    try:
        with urllib.request.urlopen(f"{google_geocode_url}?address={address}&key={google_key}") as url:
            data = json.loads(url.read().decode('utf-8'), encoding='utf-8')

            church.lat = data['results'][0]['geometry']['location']['lat']
            church.lng = data['results'][0]['geometry']['location']['lng']
            # church.save()
    except Exception as ex:
        logger.info(f'Church coordinates wasnt found: {church.title}')
        logger.error(ex.args)


def get_churches(request):
    queryset = Church.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('churches = ' + data, content_type='text/javascript')


def get_regions(request):
    queryset = Region.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('regions = ' + data, content_type='text/javascript')
