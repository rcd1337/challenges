import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Follow, Like, Post, User


def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to perform this action.")
        content = request.POST['new_post']
        username = User.objects.get(username=request.POST['username'])
        new_post = Post(content=content, username=username)
        new_post.save()

    # Shows all posts from all users, 10 per page
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    page_obj = paginator.page(page)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
    })


def following(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(f"You must be logged in to access this page.")

    # Gets all posts from users followed by 'username', 10 per page in reverse chronological order
    followingset = Follow.objects.filter(username=User.objects.get(username=current_user))
    posts = []
    if followingset:
        posts = Post.objects.filter(username=followingset[0].following)
        for user in followingset:
            posts = posts.union(Post.objects.filter(username=user.following))
        posts = posts.order_by('-id')
    paginator = Paginator(posts, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    page_obj = paginator.page(page)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    try:
        requested_username = User.objects.get(username=username)
    except:
        return HttpResponse(f" Username '{username}' not found.")
    
    # Handles number of followers/following
    followers = 0
    following = 0
    follow_network = Follow.objects.filter(username=requested_username)
    if len(follow_network) > 0:
        following = len(follow_network)
    if requested_username.followers.count() > 0:
        followers = requested_username.followers.count()

    # Determines if "current_user" is following "followed"
    try:
        Follow.objects.get(username=request.user, following=requested_username)
        follow_value = "Unfollow"
    except:
        follow_value = "Follow"

    # Gets all posts from 'username', 10 per page in reverse chronological order
    posts = Post.objects.filter(username=requested_username).order_by('-id')
    paginator = Paginator(posts, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    page_obj = paginator.page(page)

    return render(request, "network/profile.html",{
        "page_obj": page_obj,
        "requested_username": requested_username,
        "following": following,
        "followers": followers,
        "follow_value": follow_value
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# API Rountes
def edit_post(request, post_id):

    # Attempts to query requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Ensures edit is made by the post's owner
    if not request.user.id == post.username.id:
        return JsonResponse({"error": "Unauthorized action."}, status=401)

    if request.method == "GET":
        return JsonResponse({
            "content": post.content,
            "likes": post.likes
            })

    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()

        return HttpResponse(status=204)


def follow(request, followed_id):

    # Attempts query requested post
    try:
        followed = User.objects.get(pk=followed_id)
    except Follow.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    # Makes sure user is logged in
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"error": "User not logged in."}, status=404)

    # Determines if "current_user" is following "followed"
    try:
        query = Follow.objects.get(username=current_user, following=followed)
        following = True
    except Follow.DoesNotExist:
        following = False

    if request.method == "GET":
        return JsonResponse({"following": following})

    if request.method == "POST":
        if following:
            query.delete()
            followers = followed.followers.count()
            return JsonResponse({
                "was_following": following,
                "followers": followers
                })
        else:
            query = Follow(username=current_user, following=followed)
            query.save()
            followers = followed.followers.count()
            return JsonResponse({
                "was_following": following,
                "followers": followers
                })


def is_liked(request, post_id):

    # Attemps to query requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Makes sure user is logged in
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"is_liked": False})
    
    try:
        Like.objects.get(username=current_user, post=post)
        post_is_liked = True
    except Like.DoesNotExist:
        post_is_liked = False

    return JsonResponse({"is_liked": post_is_liked})


def like(request, post_id):

    #  Attempts to query requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Makes sure user is logged in
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"error": "User not logged in."}, status=404)

    # Determines if "post" is liked or not by "current_user"
    try:
        query = Like.objects.get(username=current_user, post=post)
        post_is_liked = True
    except Like.DoesNotExist:
        post_is_liked = False

    # Likes/Dislikes the queried post
    if post_is_liked:
        query.delete()
        post.likes = post.likes_received.count()
        post.save()
        return JsonResponse({
            "was_liked": post_is_liked,
            "likes": post.likes
            })
    else:
        query = Like(username=current_user, post=post)
        query.save()
        post.likes = post.likes_received.count()
        post.save()
        return JsonResponse({
            "was_liked": post_is_liked,
            "likes": post.likes
            })