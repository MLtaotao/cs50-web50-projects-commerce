from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "bid_price", "user")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "postdate", "comment")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "watchlist")

admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)