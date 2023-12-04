
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    path("newpost", views.newpost, name="newpost"),
    path("following", views.following, name="following"),
    path("like", views.likes, name="likes"),
    path("user/<str:id>", views.profile, name="profile")
]
