from django.urls import path
from . import views

app_name = "comm_polls"

urlpatterns = [
    path("", views.index, name="index"),
]
