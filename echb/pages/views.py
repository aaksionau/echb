from datetime import datetime, timedelta
import simplejson

from django.shortcuts import render, redirect, render_to_response
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext

from social_django.models import UserSocialAuth
from .models import Page, Ministry, Feedback, Video, VideoCategory, PrayerRequest
from newsevents.models import NewsItem, Event
from articles.models import Article
from .forms import FeedbackForm, PrayerRequestForm

def home(request):
    page = Page.objects.get(slug='home')
    news = NewsItem.objects.all().order_by('-publication_date')[:6]
    articles = Article.objects.all().order_by('-date').select_related('author').select_related('category')[:6]
    ministries = Ministry.objects.all()
    events = Event.objects.all().order_by('date')[:3]
    context = {
        'page': page,
        'news': news,
        'articles': articles,
        'events': events,
        'ministries': ministries
    }
    return render(request, 'pages/home.html', context)

def get_prayer_requests():
    date_delta = datetime.now() -  timedelta(days=6)
    prayer_requests_all = PrayerRequest.objects.filter(created__gte = date_delta).select_related('user').order_by('created')

    return date_delta, prayer_requests_all

def group_check(user):
    return user.groups.filter(name__in=['Admin'])


@login_required
def userprofile(request):
    prayer_requests = PrayerRequest.objects.filter(user=request.user)
    date_delta, prayer_requests_all = get_prayer_requests()

    context = {
        'prayer_requests': prayer_requests,
        'last_video_date': date_delta,
        'prayer_requests_all': prayer_requests_all
    }
    return render(request, 'profile/main.html', context)

@login_required
@user_passes_test(group_check)
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

def contacts(request):
    if request.method == 'POST':
        form=FeedbackForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['alexei.aksenov@gmail.com']
            if cc_myself:
                recipients.append(email)

            send_mail(subject, message, 'test@test.ru', recipients)
            form.save()
            return HttpResponseRedirect('/contacts/thankyou/')
        else:
            return render(request, 'pages/contacts.html', {'form':form})
    else:
        form = FeedbackForm()
        return render(request, 'pages/contacts.html', {'form':form})

def thanks(request):
    return render(request, 'pages/thankyou.html')

@login_required
def profile(request):
    return render(request, 'profile/main.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'profile/signup.html', {'form': form})

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'profile/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Ваш пароль был успешно обновлен!')
            return redirect('password')
        else:
            messages.error(request, 'Пожалуйста исправьте указанные ошибки.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'profile/password.html', {'form': form})


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