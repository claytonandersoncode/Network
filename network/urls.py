
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("compose", views.compose, name="compose"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("edit", views.edit, name="edit")
]
