from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from accounts import views

urlpatterns = [
    path('signup/', views.SignUpFormView.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', views.ProfileUserFormView.as_view(), name='profile'),
    path('profile/success/', TemplateView.as_view(template_name='accounts/profile_changed_success.html'), name='profile-success'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        html_email_template_name='accounts/password_reset_email.html', 
        subject_template_name='accounts/password_reset_subject.txt'
        ),
        name="password_reset"),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    path('prayer-requests/', views.PrayerRequestsView.as_view(), name='prayer_requests'),
    path('prayer-requests-all/', views.PrayerRequestsView.as_view(), name='prayer_requests_all'),
]