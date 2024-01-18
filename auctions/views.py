from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listings,watchlist


def index(request):
    listings = Listings.objects.all().order_by('-id')
    return render(request, "auctions/index.html",{
        "listings":listings
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

def new(request):
    categories = Category.objects.all()

    if request.method == "POST":
        listing = Listings()
        listing.title = request.POST['title']
        listing.description = request.POST['description']
        listing.image = request.FILES['image']
        listing.bid = request.POST['bid']
        listing.category = Category.objects.get(pk=request.POST['category'])
        listing.owner = User.objects.get(username=request.user)
        listing.ownerEmail=request.user.email
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/new.html",{
        "categories":categories
    })

def listing(request,id):
    try:
        watch = watchlist.objects.get(listing=id,watcher=request.user)
    except:
        watch = None
 
    if request.method == "POST":
        listing = Listings.objects.get(pk=id)
        if float(request.POST['bid'])<=float(listing.bid):
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "message":"The bid must be greater than current bid",
                "watchlist":watch,
        })
        else:
            listing.bid = request.POST['bid']
            listing.bidder = User.objects.get(username=request.user)
            listing.bidderEmail = request.user.email
            listing.save()

    listing = Listings.objects.get(pk=id)
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "watchlist":watch,
    })     

def dashboard(request):
    user_lists = Listings.objects.filter(owner=request.user)
    return render(request,"auctions/dash.html",{
        "listings":user_lists 
    })    

def watch(request):
    listings = watchlist.objects.filter(watcher=request.user)
    return render(request,"auctions/watch.html",{
        "listings":listings,
    })    

def addwatchlist(request):
    if request.method =="POST":
        add_watchlist = watchlist()
        add_watchlist.watcher = request.user
        add_watchlist.listing = Listings(id=request.POST['list_id']) 
        add_watchlist.save()
    return HttpResponseRedirect(reverse("watchlist"))    

def deleteListing(request,id):
    if request.method =="POST":
        listing = Listings.objects.get(id=id)
        listing.delete()
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))    

def closeListing(request,id):
    if request.method == "POST":
        closeBid = Listings.objects.get(id=id)
        closeBid.status = False
        closeBid.save()

        return HttpResponseRedirect(reverse("listing",args=(id,)))

    return HttpResponseRedirect(reverse("index"))    

def deleteWatch(request):
    if request.method =="POST":
        listing_id = request.POST["listing_id"]
        delWatch = watchlist.objects.get(listing=listing_id,watcher=request.user)
        delWatch.delete()
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))        