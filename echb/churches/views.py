from django.shortcuts import render, HttpResponse
from .models import Church, Region
from django.views.generic import ListView
from django.core import serializers
import urllib.request, json
from urllib.parse import quote 

def find_church(request):
    return render(request, 'churches/churches.html')

def geolocation(request):
    churches = Church.objects.all()

    for church in churches:
        address = quote(church.region.name + ' ' + church.address)
        try:
            with urllib.request.urlopen(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyAP8zWTk8oq_9o_OXwSWvkBhZ65163UXhA") as url:
                data = json.loads(url.read().decode('utf-8'), encoding='utf-8')

                church.lat = data['results'][0]['geometry']['location']['lat']
                church.lng = data['results'][0]['geometry']['location']['lng']
                #church.save()
        except:
            with open('c:/projects/echb_project/echb/churches/churches.csv', 'a', encoding='utf-8') as f:
                f.write(church.title + '\n')


def get_churches(request):
    queryset = Church.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('churches = ' + data, content_type='text/javascript')

def get_regions(request):
    queryset = Region.objects.all()
    data = serializers.serialize('json', queryset, ensure_ascii=False)
    return HttpResponse('regions = ' + data, content_type='text/javascript')


