from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Bid, Comment, Listing, User, Watchlist

import datetime



categories = ["Books, Movies & Music",
"Business & Industrial",
"Collectibles & Art",
"Electronics",
"Fashion",
"Health & Beauty",
"Home & Garden",
"Motors",
"Pet Supplies",
"Sporting Goods",
"Toys & Hobbies",
"Others"]

# cd week4sqlmm/project02/commerce

def index(request):
    listings = Listing.objects.exclude(closed=True)
    
    # Gets current logged user
    # username = None
    # if request.user.is_authenticated:
    #     username = request.user.username
    
    # Selects only currently open listings
    

    # teste = Listing.objects.exclude(closed=True).count()
    # print(teste)

    # for x in listings:
    #     if '2' in str(x.id):
    #         print(x.id)

    # # watchlist = Listing.objects.filter(owner=username)
    # # print(f"sex: {watchlist}")    

    # listing = Listing.objects.values('id').get(pk='2')
    # print(listing)

    return render(request, "auctions/index.html",{
        "listings": listings
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
                "alert_message": "Invalid username and/or password."
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
                "alert_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "alert_message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        forms = request.POST
        
        # Gets the current logged user
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        
        alert_message = []

        # Validates title
        if not forms['title']:
            alert_message.append("You must inform a title.")
        # Validates description
        if not forms['description']:
            alert_message.append("You must inform a description.")
        # Validates starting bid
        if not forms['price']:
            alert_message.append("You must inform a starting bid.")
        # Validates category
        if not forms['category']:
            alert_message.append("You must inform a category.")
        # Validates image url
        if not forms['img_url']:
            img_url = "https://i.imgur.com/Z7GSgGi.png"
        else:
            img_url = forms['img_url']
        
        if alert_message: # Returns same page with given alert alert_messages if any
            return render(request, "auctions/create_listing.html", {
            "categories": categories,
            "alert_message": alert_message
            })
        
        else: # Saves provided forms to database otherwise
            # Get current timestamp
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Creates new listing
            newlisting = Listing(title=f"{forms['title']}", description=f"{forms['description']}",
            price=f"{forms['price']}", category=f"{forms['category']}", img_url=f"{img_url}", time=time, owner=f"{username}")
            newlisting.save()
            # Returns new listing page
            return redirect(reverse('listing', args=[newlisting.id]))

    return render(request, "auctions/create_listing.html", {
    "categories": categories,
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing_id=Listing.objects.get(pk=listing_id)).count()
    comments = Comment.objects.filter(listing_id=Listing.objects.get(pk=listing_id))
    price = listing.price

    # Gets the current logged user
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    # Gets the current last bidder 
    lastbidder = None
    if bids > 0:
        lastbidder = Bid.objects.filter(listing_id=Listing.objects.get(pk=listing_id))
        lastbidder = lastbidder.order_by('-id')[0]
        lastbidder = lastbidder.username
        if lastbidder != username:
            lastbidder = None

    # Handles bidding
    if request.method == 'POST':
        bid = request.POST['bid']
        alert_message = []
        
        # Validates bid
        if not bid:
            alert_message.append(f"Your bid must be higher than the current price of ${price}.")
        elif float(bid) > float(price):
            # Get current timestamp
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            newbid = Bid(listing_id=Listing.objects.get(pk=listing_id), bid=bid, time=time, username=username)
            newbid.save()
            price = bid
            listing.price = price
            listing.save()
        else:
            alert_message.append(f"Your bid must be higher than the current price of ${price}.")
        
        # Returns same page with given alert alert_messages if any
        if alert_message:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "alert_message": alert_message,
            "bids": bids,
            "lastbidder": lastbidder
            })

    # Returns page for closed listings
    if listing.closed == True:
        winner = Bid.objects.filter(listing_id=Listing.objects.get(pk=listing_id))
        if not winner:
            winner = "No bids were placed."
        else:
            winner = winner.order_by('-id')[0]
            winner = winner.username
        
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "winner": winner,
        "bids": bids,
        "lastbidder": lastbidder
        })
    
    # Returns page for open listings
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "comments": comments,
    "bids": bids,
    "lastbidder": lastbidder
    })
    

@login_required
def watchlist(request):
    # Gets the current logged user
    username = None
    if request.user.is_authenticated:
        username = request.user.username   
    
    watchlist = Watchlist.objects.filter(username=username)
    
    # Handles "Whatchlist" button
    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        comments = Comment.objects.filter(listing_id=Listing.objects.get(pk=listing.id))
        
        # Gets the "winner" in case the listing is closed
        winner = "No winners yet."
        if listing.closed == True:
            winner = Bid.objects.filter(listing_id=Listing.objects.get(pk=listing.id))
            if not winner:
                winner = "No bids were placed."
            else:
                winner = winner.order_by('-id')[0]
                winner = winner.username
            
        add_to_watchlist = True

        # Analyzes if listing is already watchlisted
        for row in watchlist:
            if listing == row.listing_id:
                add_to_watchlist = False
        
        # Adds item to watchlist OR deletes item from watchlist if already in it
        if add_to_watchlist == True:
            newitem = Watchlist(listing_id=Listing.objects.get(pk=listing.id), username=f"{username}")
            newitem.save()
            watchlist_message = f'"{listing.title}" was added to your watchlist.'
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "winner": winner,
            "watchlist_message": watchlist_message
        })
        else:
            item = Watchlist.objects.get(listing_id=Listing.objects.get(pk=listing.id), username=username)
            item.delete()
            watchlist_message = f'"{listing.title}" was removed from your watchlist.'
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "winner": winner,
            "watchlist_message": watchlist_message
        })
    # Renders current watchlist [GET]
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
        })


def cats(request):
    return render(request, "auctions/categories.html",{
        "categories": categories
    })


def cat(request, category):
    # Gets the category sent by "cats" via URL and returns only the listings of the giving category
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })

def submit_comment(request):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        comment = request.POST['comment']

        # Gets the current logged user
        username = None
        if request.user.is_authenticated:
            username = request.user.username

        # Saves comment if valid
        if not comment:
            return redirect(reverse('listing', args=[listing.id]))
        else:
            # Get current timestamp
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            newcomment = Comment(listing_id=Listing.objects.get(pk=listing.id), comment=f"{comment}", time=time, username=username)
            newcomment.save()
            return redirect(reverse('listing', args=[listing.id]))


def close_listing(request):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        
        # Gets the current logged user
        username = None
        if request.user.is_authenticated:
            username = request.user.username

        if listing.owner == username and listing.closed == False:
            listing.closed = True
            listing.save()

        return redirect(reverse('listing', args=[listing.id]))