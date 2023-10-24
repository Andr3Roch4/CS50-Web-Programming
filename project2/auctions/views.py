from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Comments, Bids, Categories


def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def list(request):
    if request.method == "POST":
        list = Listings(name=request.POST["name"], pricetag=request.POST["pricetag"], description=request.POST["description"], startingbid=request.POST["startingbid"], image=request.POST["img"])
        list.clean_fields()
        list.save()
        category = Categories(category=request.POST["category"], item=Listings.objects.get(pk=list.id))
        category.clean_fields()
        category.save()
        return HttpResponseRedirect(reverse("listing", args=[list.id]))
    else:
        return render(request, "auctions/list.html")
    
def listing(request, list_id):
    item = Listings.objects.get(pk=list_id)
    highestbid = item.highestbid()
    return render(request, "auctions/listing.html", {
        "item": item,
        "category": item.category.all(),
        "highestbid": highestbid
    })

@login_required    
def watchlist(request):
    watchlist = User.user_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def category(request):
    category = Categories.objects.all()
    return render(request, "auctions/category.html", {
        "category": category
    })

#admin/admin123