from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "App"

urlpatterns = [
    path("", views.login, name="login"),
    path("all-videos", views.videos, name="videos"),
    path("play/<slug>", views.VideoDetailView.as_view(), name="details"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("enroll", views.enroll, name="enroll"),
    path("verify", views.verify, name="verify"),


]
