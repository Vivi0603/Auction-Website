from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    categoryName = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.categoryName}"

class Listings(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owenerr")
    ownerEmail = models.CharField(max_length=255)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bidderr",null=True,blank=True)
    bidderEmail = models.CharField(max_length=255)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    #image = models.CharField(max_length=255)
    image = models.ImageField(upload_to='listingsImages/')
    bid = models.FloatField()
    status = models.BooleanField(default=True)
    

class watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE,null=True,blank=True)

