
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    path("newpost", views.newpost, name="newpost"),
    path("<str:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<str:id>", views.likes, name="likes")
]
