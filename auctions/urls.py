from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mywatchlist", views.my_watchlist, name="mywatchlist"),
    path("category/<str:category_id>", views.watch_category, name='category'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creat", views.creat, name="creat"),
    path("addwatchlist/<str:user_id>/<str:auction_id>", views.add_watchlist, name='addwatchlist'),
    path("delwatchlist/<str:user_id>/<str:auction_id>", views.del_watchlist, name='delwatchlist'),
    path("addbid/<str:user_id>/<str:auction_id>", views.add_bid, name='addbid'),
    path("addcomment/<str:user_id>/<str:auction_id>", views.add_comment, name='addcomment'),
    path("listing/<str:auction_id>", views.listing, name="listing"),
    path("closebid/<str:auction_id>", views.close_bid, name="closebid")
]
