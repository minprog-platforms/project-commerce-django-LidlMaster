from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass
    # phone = models.PositiveIntegerField(max_length=10)

class Category(models.Model):
    categoryName = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.categoryName

class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid" )
    bid = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.bid)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    # For image use URL --> text
    imageUrl = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice" )
    # currentbid = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="bid")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    #  Lecture notes Many to many realationships-->
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self) -> str:
        return self.title
        
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.commenter} comment on {self.listing}"