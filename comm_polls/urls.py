from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "comm_polls"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("account_settings/", views.account_settings, name="account_settings"),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
