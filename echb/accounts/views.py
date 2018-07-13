from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from django.shortcuts import render
from django.views.generic.edit import FormView

from pages.models import OldUser

class SignUpFormView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/online/'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super(SignUpFormView, self).form_valid(form)

class LoginUser(LoginView):
    template_name = 'accounts/login.html'

def profile(request):
    pass

def settings(request):
    pass

