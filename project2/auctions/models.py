from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime


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
        ("VideoGames", "Video Games")
    ]
    category = models.CharField(max_length=64, choices=categories)

class Listings(datetime, models.Model):
    name = models.CharField(max_length=64)
    pricetag = models.PositiveIntegerField
    description = models.TextField(max_length=200)
    startingbid = models.PositiveIntegerField
    image = models.URLField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name="item")

    def highestbid(self):
        if not self.bids:
            return "No bid on this item yet."
        else:
            highestbid = self.bids.order_by("bid").desc()[0]
            return highestbid

class Bids(datetime, models.Model):
    bid = models.PositiveIntegerField
    time = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")

class Comments(datetime, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=200)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")

    class Watchlist(models.Model):
        item = models.ManyToManyField(Listings, related_name="watchlist")
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")



