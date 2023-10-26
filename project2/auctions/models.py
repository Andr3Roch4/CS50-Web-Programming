from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Categories(models.Model):
    categories = [
        ("Automotive", "Automotive"),
        ("Beauty", "Beauty"),
        ("BabyProducts", "Baby Products"),
        ("Books", "Books"),
        ("Camera", "Camera"),
        ("CellPhones", "Cell Phones"),
        ("Eletronics", "Eletronics"),
        ("FineArt", "Fine Art"),
        ("Foods", "Foods"),
        ("HealthCare", "Health Care"),
        ("Home", "Home"),
        ("Music", "Music"),
        ("Ofice", "Ofice"),
        ("Outdoors", "Outdoors"),
        ("Sports", "Sports"),
        ("Toys", "Toys"),
        ("Video", "Video"),
        ("VideoGames", "Video Games"),
        ("None", "Not Specified")
    ]
    category = models.CharField(max_length=64, choices=categories, unique=True)

class Listings(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=400)
    startingbid = models.PositiveIntegerField()
    image = models.URLField(max_length=200, blank=True)
    time = models.DateTimeField(default=datetime.datetime.now())
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name="item", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    isclosed = models.BooleanField(default=False)

    @property
    def highestbid(self):
        if self.bids.all() == None:
            return self.startingbid
        else:
            highestbid = self.bids.all()
            highestbid = highestbid.order_by("bid").last()
            return highestbid

class Bids(models.Model):
    bid = models.PositiveIntegerField()
    time = models.DateTimeField(default=datetime.datetime.now())
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    time = models.DateTimeField(default=datetime.datetime.now())
    comment = models.TextField(max_length=400)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")

class Watchlist(models.Model):
    item = models.ManyToManyField(Listings, blank=True, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")



