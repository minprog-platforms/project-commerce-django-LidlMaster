from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass
    # phone = models.PositiveIntegerField(max_length=10)

class Category(models.Model):
    grouping = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.grouping


class Listing(models.Model):
    title = models.CharField(max_length=64)
    # For image use URL --> text
    image = models.CharField(max_length=1000) 
    date = models.DateTimeField(default=datetime.now, blank=True)
    price = models.FloatField()
    # currentbid = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="bid")
    activelisting = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingsWatchlist")

    def __str__(self) -> str:
        return self.title
        
# class Bids(models.Model):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user" )
#     bid = models.FloatField()


# class Comments(models.Model):
#     commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User")
#     comment = models.CharField(max_length=500)
