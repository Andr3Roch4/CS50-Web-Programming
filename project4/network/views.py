from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator

from .models import User, Posts, Followers, Likes


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def allposts(request):
    if request.method == "POST":
        data = json.load(request.body)
        if data.get("editcontent") and data.get("postid") is not None:
            try:
                user = User.objects.get(pk=request.user.id)
            except:
                return JsonResponse({"message": "Must be logged in to edit your post."}, status=401)
            if data.get("postid") in user.posts.id.all():
                post = Posts.objects.get(pk=data.get("postid"))
                post.content = data.get("editcontent")
                post.save()
            else:
                return JsonResponse({"message": "Can only edit your posts."}, status=402)
    else:
        posts = Posts.objects.all().order_by("-time")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/allposts.html", {
            "posts": page_obj
        })

@login_required
def newpost(request):
    # When new post form is submited, save post 
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        post = Posts(user=user, content=request.POST["content"])
        post.save()
        likes = Likes(post=Posts.objects.get(pk=post.id))
        likes.save()
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def profile(request, id):
    user = User.objects.get(pk=id)
    posts = user.posts.all().order_by("-time")
    followers = Followers.followers.filter(user=user).count()
    follows = Followers.follows.filter(user=user).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "user": user,
        "posts": page_obj,
        "follows": follows,
        "followers": followers
    })

@login_required
def following(request):
    user = User.objects.get(pk=request.user.id)
    userfollows = user.follows.all()
    posts = Posts.objects.filter(user__in=userfollows)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/allposts.html", {
        "posts": page_obj
    })

@login_required
def likes(request, id):
    if request.method == "PUT":
        post = Posts.objects.get(pk=id)
        data = json.loads(request.body)
        if data.get("like") is not None:
            likes = Likes.objects.get(post=post)
            likes.likes = + int(data.get("like"))
            user = User.objects.get(pk=request.user.id)
            if likes.users.get(id=user.id):
                likes.users.remove(user)
            else:
                likes.users.add(user)
            likes.save()
        return JsonResponse({"message": "Post liked!"}, status=201)
    else:
        return HttpResponseRedirect(reverse("index"))
