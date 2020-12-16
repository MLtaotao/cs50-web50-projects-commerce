from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Auction, Bid, Comment, Watchlist
from .forms import ListingForm
from datetime import datetime
import pytz
#from .util import add_watchlist



def index(request):
    auctions = Auction.objects.filter(start_time__lte= datetime.now(), sell_button= False).order_by('-start_time')
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': auctions,
        'categories': categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
        
@login_required(login_url= "login")
def creat(request):
    if request.method == "POST":
        #上传input内容
        pforms = ListingForm(request.POST)
        if pforms.is_valid():
            f = Auction(user= request.user, 
            title= pforms.cleaned_data['title'], category= pforms.cleaned_data['category'], 
            description= pforms.cleaned_data['description'], start_time= pforms.cleaned_data['start_time'], 
            price= pforms.cleaned_data['price'], img_url= pforms.cleaned_data['img_rul'])
            f.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form = ListingForm()
            return render(request, "auctions/creat1.html", {
                'form': form
            })
    else:
        form = ListingForm()
        return render(request, "auctions/creat1.html", {
            # "category": Category.objects.all().values_list('category', flat=True)
            'form': form
        })

def watch_category(request, category_id):
    auctions = Auction.objects.filter(category= category_id)
    return render(request, "auctions/category.html", {
    'auctions': auctions
    })

@login_required(login_url= "login")
def my_watchlist(request):
    watchlists = Watchlist.objects.filter(user= request.user).values_list('watchlist')
    auctions = Auction.objects.filter(id__in = watchlists)
    return render(request, "auctions/mywatchlist.html", {
    'auctions': auctions
    })

@login_required(login_url= "login")        
def listing(request, auction_id):
    auction = Auction.objects.get(id = auction_id)
    #使用watchlist button判断，如果为真，则展示删除按钮，如果为假，则展示增加按钮
    watchlist_button = Watchlist.objects.filter(user= request.user, watchlist= auction).exists()
    comments = Comment.objects.filter(auction= auction).order_by('-postdate')
    return render(request, "auctions/listing.html", {
        'auction': auction,
        'watchlist_button': watchlist_button,
        'comments': comments
    })
@login_required(login_url= "login")
def add_watchlist(request, user_id, auction_id):
    w = Watchlist(user= User.objects.get(id = user_id), watchlist= Auction.objects.get(id = auction_id))
    w.save()
    return HttpResponseRedirect(reverse('listing', args= (auction_id)))

@login_required(login_url= "login")
def del_watchlist(request, user_id, auction_id):
    w = Watchlist.objects.filter(user= User.objects.get(id = user_id), watchlist= Auction.objects.get(id = auction_id))
    w.delete()
    return HttpResponseRedirect(reverse('listing', args= (auction_id)))
@login_required(login_url= "login")
def add_bid(request, user_id, auction_id):
    user = User.objects.get(id = user_id)
    auction = Auction.objects.get(id = auction_id)
    if request.method == "POST":
        if request.POST.get('bidprice') == '':
            watchlist_button = Watchlist.objects.filter(user= user, watchlist= auction).exists()
            return render(request, "auctions/listing.html", {
                'auction': auction,
                'watchlist_button': watchlist_button,
                'bid_message': "ERROR: Must input your price and then for bid!!!"
            })
        elif int(request.POST.get('bidprice')) <= auction.price:
            watchlist_button = Watchlist.objects.filter(user= user, watchlist= auction).exists()
            return render(request, "auctions/listing.html", {
                'auction': auction,
                'watchlist_button': watchlist_button,
                'bid_message': "ERROR: The price must be greater than the currnet price!!!"
            })
        else:
            bid = Bid(user = user, auction= auction, bid_price= int(request.POST.get('bidprice')))
            bid.save()
            auction.price = bid.bid_price
            auction.save()
            return HttpResponseRedirect(reverse('listing', args= (auction_id)))
    else:
        return HttpResponseRedirect(reverse('listing', args= (auction_id)))

@login_required(login_url= "login")
def add_comment(request, user_id, auction_id):
    user = User.objects.get(id = user_id)
    auction = Auction.objects.get(id = auction_id)
    if request.method == "POST":
        if request.POST.get('comment') == '':
            return HttpResponseRedirect(reverse('listing', args= (auction_id)))
        else:
            comment = Comment(user= user, auction= auction, comment= request.POST.get('comment'), postdate= datetime.now())
            comment.save()
            return HttpResponseRedirect(reverse('listing', args= (auction_id)))
    else:
        return HttpResponseRedirect(reverse('listing', args= (auction_id)))

@login_required(login_url= "login")
def close_bid(request, auction_id):
    auction = Auction.objects.get(id = auction_id)
    auction.sell_button = True
    winbid= Bid.objects.filter(auction= auction).order_by('-bid_price').first()
    auction.winner = winbid.user
    auction.price = winbid.bid_price
    auction.save()
    return HttpResponseRedirect(reverse('listing', args= (auction_id)))

