from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import User, Listings, Comments, Bids, Categories, Watchlist
from .forms import ListingsForm, CategoriesForm, CommentForm


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

@login_required(login_url="login")
def list(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        form = ListingsForm(request.POST)
        form2 = CategoriesForm(request.POST)
        if form.is_valid() and form2.is_valid():
            try:
                list_category = Categories.objects.get(category=form2.cleaned_data["category"])
            except:
                category = Categories(category=form2.cleaned_data["category"])
                category.clean_fields()
                category.save()
                list_category = Categories.objects.get(category=form2.cleaned_data["category"])
            list = Listings(
                name=form.cleaned_data["name"], 
                description=form.cleaned_data["description"], 
                startingbid=form.cleaned_data["startingbid"], 
                image=form.cleaned_data["image"], 
                user=user, 
                category=list_category, 
                time=datetime.datetime.now()
                )
            list.clean_fields()
            list.save()
            item = Listings.objects.get(pk=list.id)
            bid = Bids(bid=form.cleaned_data["startingbid"], item=item, user=user, time=datetime.datetime.now())
            bid.clean_fields()
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=[list.id]))
        else: 
            return render(request, "auctions/list.html", {
            "form": form,
            "form2": form2
        })
    else:
        form = ListingsForm()
        form2 = CategoriesForm()
        return render(request, "auctions/list.html", {
            "form": form,
            "form2": form2
        })

def listing(request, list_id):
    item = Listings.objects.get(pk=list_id)
    if item.isclosed is True:
        if item.highestbid.user.id == request.user.id:
            won = True
        else:
            won = None
        return render(request, "auctions/closedlisting.html", {
            "item": item,
            "won": won
        })
    elif request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        item_by_user = item.user
        try:
            watchlist = Watchlist.objects.get(user=user)
            item_in_watchlist = watchlist.item.get(pk=list_id)
        except:
            item_in_watchlist = False
        if item.user == user:
            item_by_user = user.listings.get(pk=list_id)
        else:
            item_by_user = False
        if item.highestbid.bid >= int(request.POST["bid"]):
            number_bids = item.bids.count() - 1
            comments = item.comments.all()
            form = CommentForm()
            return render(request, "auctions/listing.html", {
            "item": item,
            "bids": number_bids,
            "comments": comments,
            "error_message": "Your bid must be higher the the current bid.",
            "form": form,
            "item_in_watchlist": item_in_watchlist,
            "item_by_user": item_by_user
        })
        else:
            bid = Bids(bid=request.POST["bid"], item=item, user=user, time=datetime.datetime.now())
            bid.clean_fields()
            bid.save()
        item = Listings.objects.get(pk=list_id)
        number_bids = item.bids.count() - 1
        comments = item.comments.all()
        form = CommentForm()
        youbid = "Your bid has been placed, and is now the highest bid."
        return render(request, "auctions/listing.html", {
            "item": item,
            "bids": number_bids,
            "youbid": youbid,
            "comments": comments,
            "form": form,
            "item_in_watchlist": item_in_watchlist,
            "item_by_user": item_by_user
        })
    else:
        try:
            user = User.objects.get(pk=request.user.id)
            watchlist = Watchlist.objects.get(user=user)
            item_in_watchlist = watchlist.item.get(pk=list_id)
            
        except:
            item_in_watchlist = None
            item_by_user = None
        try:
            user = User.objects.get(pk=request.user.id)
            item_by_user = user.listings.get(pk=list_id)
        except:
            item_by_user = None
        number_bids = item.bids.count() - 1
        comments = item.comments.all()
        form = CommentForm()
        return render(request, "auctions/listing.html", {
            "item": item,
            "bids": number_bids,
            "comments": comments,
            "form": form,
            "item_in_watchlist": item_in_watchlist,
            "item_by_user": item_by_user
        })

@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        item = Listings.objects.get(pk=request.POST["id"])
        try:
            watchlist = Watchlist.objects.get(user=user)
        except:
            watchlist = Watchlist.objects.create(user=user)
        if item in watchlist.item.all():
            watchlist.item.remove(item)
        else:
            watchlist.item.add(item)
        return HttpResponseRedirect(reverse("listing", args=[request.POST["id"]]))
    else:
        user = User.objects.get(pk=request.user.id)
        try:
            watchlist = Watchlist.objects.get(user=user)
            items = watchlist.item.all()
        except:
            items = None
        return render(request, "auctions/watchlist.html", {
            "items": items
        })

@login_required(login_url="login")
def category(request):
    if request.method == "POST":
        form = CategoriesForm(request.POST)
        if form.is_valid():
            try:
                category = Categories.objects.get(category=form.cleaned_data["category"])
                items = category.item.all().exclude(isclosed=True)
                if not items:
                    return render(request, "auctions/category.html", {
                        "form": form,
                        "error_message": "No listings on selected category."
                    })
                else:
                    return render(request, "auctions/category.html", {
                        "items": items,
                        "category": category
                    })
            except:
                return render(request, "auctions/category.html", {
                    "form": form,
                    "error_message": "No listings on selected category."
                })
    else:
        form = CategoriesForm()
        return render(request, "auctions/category.html", {
            "form": form
        })

@login_required(login_url="login")
def mylistings(request):
    user = User.objects.get(pk=request.user.id)
    listings = user.listings.all()
    return render(request, "auctions/mylistings.html", {
        "listings": listings
    })

@login_required(login_url="login")
def mybids(request):
    user = User.objects.get(pk=request.user.id)
    user_items = user.listings.all()
    bids = user.user_bids.all().order_by("-time")
    return render(request, "auctions/mybids.html", {
        "bids": bids
    })

@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        comment_text = request.POST["comment"]
        item = Listings.objects.get(pk=request.POST["itemid"])
        comment = Comments(user=user, item=item, comment=comment_text, time=datetime.datetime.now())
        comment.clean_fields()
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=request.POST["itemid"]))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="login")
def removelisting(request):
    if request.method == "POST":
        item = Listings.objects.get(pk=request.POST["id"])
        item.isclosed = True
        item.save()
        return HttpResponseRedirect(reverse("listing", args=request.POST["id"]))
    else:
        return HttpResponseRedirect(reverse("index"))
    
#admin/admin123