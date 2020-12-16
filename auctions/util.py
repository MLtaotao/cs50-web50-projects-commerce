from .models import Auction, User, Watchlist


def add_watchlist(user, auction):
    w = Watchlist(user, auction)
    w.save()