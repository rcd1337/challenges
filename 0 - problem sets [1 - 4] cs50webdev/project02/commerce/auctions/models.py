from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Listing(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    category = models.CharField(max_length=32)
    img_url = models.CharField(max_length=500, default="no_img")
    time = models.CharField(max_length=30, default='unknown')
    owner = models.CharField(max_length=64, default=None)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"ID:{self.id} Title:{self.title} Description:{self.description} Starting bid:{self.price} Category:{self.category} Img_url:{self.img_url} Time:{self.time} Owner:{self.owner} BOOL:{self.closed}\n"

    objects = models.Manager()


class Bid(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", default=None)
    bid = models.DecimalField(max_digits=14, decimal_places=2, default=None)
    time = models.CharField(max_length=30, default='unknown')
    username = models.CharField(max_length=64, default=None)
    
    objects = models.Manager()

    def __str__(self):
        return f"ID: {self.id} BID: {self.bid} TIME: {self.time} BIDDER: {self.username}"

class Comment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default=None)
    comment = models.TextField(max_length=2000, default=None)
    time = models.CharField(max_length=30, default='unknown')
    username = models.CharField(max_length=64, default=None)
    
    objects = models.Manager()

    def __str__(self):
        return f"ID:{self.id} LISTING_ID:{self.listing_id} COMMENT:{self.comment} TIME:{self.time} USERNAME:{self.username}"


class Watchlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watch", default=None)
    username = models.CharField(max_length=64, default=None)

    objects = models.Manager()

    def __str__(self):
        return f"ID:{self.id} LISTING_ID:{self.listing_id} USERNAME:{self.username}"