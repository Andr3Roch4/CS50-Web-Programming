from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search/", views.searchresult, name="search"),
    path("random/", views.randomtitle, name="random")
    ]
