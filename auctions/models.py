from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length= 64, unique= True)
    def __str__(self):
        return self.category

class Auction(models.Model):
    title = models.CharField(max_length= 64)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="founder")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length= 500)
    start_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    img_url = models.URLField()
    sell_button = models.BooleanField(default = False)
    winner = models.ForeignKey(User, on_delete= models.CASCADE, related_name="buyer", default= '', null= True)
    def __str__(self):
        return(f"{self.id}: {self.title} begins at {self.start_time} with ${self.price}")


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    # bid_price = models.PositiveIntegerField(default = auction.price, validators= [MinValueValidator(auction.price)])
    bid_price = models.PositiveIntegerField()

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE)
    postdate = models.DateTimeField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    watchlist = models.ForeignKey(Auction, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['user', 'watchlist'], name= 'user-auction')
        ]
        