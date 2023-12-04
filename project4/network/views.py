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
            following = Followers(user=User.objects.get(pk=user.id))
            following.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def allposts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newcontent = data.get("newcontent")
        print(newcontent)
        postid = data.get("postid")
        user = User.objects.get(pk=request.user.id)
        userposts = Posts.objects.filter(user=user)
        post = Posts.objects.get(pk=postid)
        if post in userposts:
            post.content = newcontent
            post.save()
            return JsonResponse({"newcontent": newcontent})
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


@login_required(login_url="login")
def newpost(request):
    # When new post form is submited, save post 
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        post = Posts(user=user, content=request.POST["content"])
        post.save()
        likes = Likes(post=Posts.objects.get(pk=post.id))
        likes.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def profile(request, id):
    user = User.objects.get(pk=id)
    posts = user.posts.all().order_by("-time")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "poster": user,
        "posts": page_obj,
    })


@csrf_exempt
@login_required(login_url="login")
def following(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(pk=request.user.id)
        userf = User.objects.get(pk=data.get("id"))
        userfollows = user.following.follows.all()
        if userf in userfollows:
            follow = Followers.objects.get(user=user)
            follow.follows.remove(userf)
            follow.save()
            following = Followers.objects.get(user=userf)
            following.followers.remove(user)
            return JsonResponse({"message": f"Unfollowed {userf.username}", "follow": "Follow"})
        elif userf not in userfollows:
            follow = Followers.objects.get(user=user)
            follow.follows.add(userf)
            follow.save()
            following = Followers.objects.get(user=userf)
            following.followers.add(user)
            following.save()
            return JsonResponse({"message": f"Now following {userf.username}", "follow": "Unfollow"})
    else:
        user = User.objects.get(pk=request.user.id)
        follows = Followers.objects.get(user=user)
        userfollows = follows.follows.all()
        posts = Posts.objects.filter(user__in=userfollows)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html", {
            "posts": page_obj
        })


@csrf_exempt
@login_required(login_url="login")
def likes(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("id"), data.get("like"))
        post = Posts.objects.get(pk=data.get("id"))
        if data.get("like") == "1" or "-1":
            likes = Likes.objects.get(post__id=post.id)
            likes.like += int(data.get("like"))
            user = User.objects.get(pk=request.user.id)
            if data.get("like") == "-1":
                likes.users.remove(user)
                liked = False
            elif data.get("like") == "1":
                likes.users.add(user)
                liked = True
            likes.save()
            print(liked)
            return JsonResponse({"data": likes.like, "liked": liked}, safe=False)
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

