from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    def __str__(self):
        return self.username
    #pass
    #likes = models.ManyToManyField("Likes", null=True, related_name="userlikes")

class Posts(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT)
    content = models.TextField(max_length=400)
    time = models.DateTimeField(auto_now_add=True)
    #@property
    #def liked(self, request):
        #if request.user in self.postlikes.users:
            #return True
        #return False
    #likes = models.ForeignKey("Likes", on_delete=models.CASCADE, related_name="postlikes")

class Followers(models.Model):
    followers = models.ManyToManyField(User, blank=True, null=True, related_name="followers")
    user = models.OneToOneField(User, related_name="following",on_delete=models.CASCADE, null=True)
    follows = models.ManyToManyField(User, blank=True, null=True, related_name="follows")

class Likes(models.Model):
    post = models.OneToOneField(Posts, on_delete=models.CASCADE, related_name="postlikes", null=True)
    like = models.IntegerField(default=0)
    users = models.ManyToManyField(User, null=True, blank=True)
