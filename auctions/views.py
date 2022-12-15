from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Bid, Listing, Comment


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings":  activeListings,
        "categories" : allCategories
    })

def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.get(categoryName=categoryFromForm)
    activeListings = Listing.objects.filter(isActive=True, category=category)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings":  activeListings,
        "categories" : allCategories
    })

def createListing(request):
    if request.method == "GET":
        # Lecture notes
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        #entry options from form
        title = request.POST["title"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST["category"]
        description = request.POST["description"]
        #logged in user
        currentUser = request.user
        categoryData = Category.objects.get(categoryName=category)
        # bid object
        bid = Bid(bid=float(price), user=currentUser)
        bid.save()
        #listing -- Lecture notes --        
        newListing = Listing( 
            title=title,
            imageUrl=imageUrl,
            owner=currentUser,
            price=bid,
            category=categoryData,
            description=description
        )
        #save into datbase
        newListing.save()
        #show on page
        return HttpResponseRedirect(reverse(index))

def listing (request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist":isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })

def addBid(request, id):
    listingData = Listing.objects.get(pk=id)
    newBid = request.POST['newBid']
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if float(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=float(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid posted succesfully",
            "update": True,
            "isListingInWatchlist":isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Failed to post Bid, entered amount not enough",
            "update": False,
            "isListingInWatchlist":isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,

        })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist":isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Auction closed succesfully"
    })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    comment = request.POST['newComment']
    newComment = Comment(
        commenter = currentUser,
        listing = listingData,
        comment = comment
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

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
