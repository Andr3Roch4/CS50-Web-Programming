from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    liked = models.ForeignKey("Likes", on_delete=models.PROTECT, related_name="users", null=True)

class Posts(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT)
    content = models.TextField(max_length=400)
    time = models.DateTimeField(auto_now_add=True)

class Followers(models.Model):
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    user = models.ForeignKey(User, related_name="following",on_delete=models.CASCADE)
    follows = models.ManyToManyField(User, blank=True, related_name="follows")

class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")
    like = models.PositiveIntegerField(default=0)
