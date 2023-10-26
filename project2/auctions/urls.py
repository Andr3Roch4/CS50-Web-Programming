from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list", views.list, name="list"),
    path("listing/<str:list_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("mybids", views.mybids, name="mybids"),
    path("comment", views.comment, name="comment"),
    path("removelisting", views.removelisting, name="removelisting")
]
