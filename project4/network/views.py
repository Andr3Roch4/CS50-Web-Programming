from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, Followers, Likes


def index(request):
    return HttpResponseRedirect(reverse("allposts"))


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
        newcontent = request.POST["newcontent"]
        postid = request.POST["postid"]
        user = User.objects.get(pk=request.user.id)
        userposts = Posts.objects.filter(user=user)
        post = Posts.objects.get(pk=postid)
        if post in userposts:
            post.content = newcontent
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        posts = Posts.objects.all().order_by("-time")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj
        })

@login_required
def newpost(request):
    # When new post form is submited, save post 
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        like = Likes()
        like.save()
        post = Posts(user=user, content=request.POST["content"], likes=Likes.objects.get(pk=like.id))
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def profile(request, id):
    user = User.objects.get(pk=id)
    posts = user.posts.all().order_by("-time")
    followers = user.followers.filter(user=user).count()
    follows = user.follows.filter(user=user).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "poster": user,
        "posts": page_obj,
        "follows": follows,
        "followers": followers
    })

@login_required
def following(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(pk=request.user.id)
        userf = User.objects.get(pk=data.get("id"))
        userfollows = user.follows.all()
        if userf.id in userfollows.id:
            user.follows.remove(userf)
            user.save()
            userf.followers.remove(user)
            userf.save()
            return JsonResponse({"message": f"Unfollowed {userf.username}"})
        elif userf.id not in userfollows.id:
            user.follows.add(userf)
            user.save()
            userf.followers.add(user)
            userf.save()
            return JsonResponse({"message": f"Now following {userf.username}"})
    else:
        user = User.objects.get(pk=request.user.id)
        try:
            follows = Followers.objects.get(user=user)
            userfollows = follows.follows.all()
            posts = Posts.objects.filter(user__in=userfollows)
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "network/following.html", {
                "posts": page_obj
            })
        except:
            return render(request, "network/following.html")

@csrf_exempt
@login_required
def likes(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Posts.objects.get(pk=data.get("id"))
        if data.get("like") == "1" or "-1":
            likes = Likes.objects.get(pk=post.likes.id)
            likes.like = +int(data.get("like"))
            user = User.objects.get(pk=request.user.id)
            if data.get("like") == "-1":
                likes.users.remove(user)
                likes.save()
                return JsonResponse({"data": likes.like}, safe=False)
            else:
                likes.users.add(user)
                likes.save()
                return JsonResponse({"data": likes.like}, safe=False)
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def editpost(request, id):
    post = Posts.objects.get(pk=id)
    return render(request, "network/editpost.html", {
        "post": post
    })