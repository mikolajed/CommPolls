from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = "comm_polls"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("account_settings/", views.account_settings, name="account_settings"),
    path('polls/', views.polls_list, name='polls'),        
    path('votes/', views.my_votes, name='votes'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/<int:poll_id>/manage/', views.manage_poll, name='manage_poll'),
    path('polls/<int:poll_id>/vote/', views.vote, name='vote'),
    path('polls/<int:poll_id>/results/', views.results, name='results'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            success_url=reverse_lazy('comm_polls:password_change_done')
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
