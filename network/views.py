import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms

from .models import User, Post, Like, Follow

class ComposeForm(forms.Form):
    body = forms.CharField(label=False, max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Post', 'id': 'compose-body', 'cols': 200,
        'rows': 3,}))
    

def index(request):

    #Get post objects and order them
    posts = Post.objects.all()
    posts = posts.order_by("-date").all()
    
    #Filter posts for objects where user has liked posts (to display in templates on page load)
    post_list = []
    for post in posts:
        if request.user.is_authenticated:
            post_list.append((post, Like.objects.filter(who_liked=request.user, what_post=post)))
        else:
            post_list.append((post, False))

    #Paginate results
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'composeform': ComposeForm()
    })

@login_required
def compose(request):

    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = ComposeForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the variables from the 'cleaned' version of form data
            body = form.cleaned_data["body"]
            who_created = request.user

            # Create a listing object and a bid object related to it
            post = Post(body=body, who_created=who_created)
            post.save()

            # Redirect user to index
            return HttpResponseRedirect(reverse("index"))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "network/index.html", {
                "composeform": form
            })


@csrf_exempt
@login_required
def like(request):

    # Liking a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get Post
    data = json.loads(request.body)
    post = Post.objects.get(id=data)
    
    # Check if user already likes post
    is_liked = Like.objects.filter(who_liked=request.user, what_post=post)
    if is_liked:
        is_liked.delete()
        is_liked = False
    else:
        # Create a like object
        like = Like(
            who_liked=request.user,
            what_post=post,
        )
        like.save()
        is_liked = True

    # Check total likes
    total_likes = len(Like.objects.filter(what_post=post))

    return JsonResponse({"total_likes": total_likes, "is_liked": is_liked}, status=201)

@csrf_exempt
@login_required
def follow(request):

    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get user to follow
    data = json.loads(request.body)
    user = User.objects.get(id=data)
    
    # Check if user already follows
    is_followed = Follow.objects.filter(follower=request.user,is_following=user)
    if is_followed:
        is_followed.delete()
        is_followed = False
    else:
        # Create a follow object
        follow = Follow(
            follower=request.user,
            is_following=user,
        )
        follow.save()
        is_followed = True

    # Check total follows
    total_follows = len(Follow.objects.filter(is_following=user))

    return JsonResponse({"total_follows": total_follows, "is_followed": is_followed}, status=201)

@csrf_exempt
@login_required
def edit(request):

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of post
    data = json.loads(request.body)
    id = data.get("id", "")
    updated_body = data.get("body", "")

    # Edit post object
    post = Post.objects.get(id=id)
    post.body = updated_body
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)
   
def profile(request, username):
    
    #Get User 
    profile = User.objects.get(username=username)
    
    #Get Followers and Following
    followers = len(Follow.objects.filter(is_following=profile))
    following = len(Follow.objects.filter(follower=profile))

    # Check if request.user already follows
    if request.user.is_authenticated:
        is_followed = Follow.objects.filter(follower=request.user,is_following=profile)
    else:
        is_followed = False

    #Get post for user and order them
    posts = Post.objects.filter(who_created=profile)
    posts = posts.order_by("-date").all()

    #Filter posts for objects where user has liked posts (to display in templates on page load)
    post_list = []
    for post in posts:
        if request.user.is_authenticated:
            post_list.append((post, Like.objects.filter(who_liked=request.user, what_post=post)))
        else:
            post_list.append((post, False))    

    #Paginate results
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "profile": profile,
        'page_obj': page_obj,
        "followers": followers,
        "following": following,
        "is_followed": is_followed
    })

@login_required
def following(request):
    
    #Get post objects where user follows a list of users 
    user = request.user
    
    follow_list = []
    following = Follow.objects.filter(follower=user)
    for person in following:
        follow_list.append(person.is_following)
    
    posts = Post.objects.filter(who_created__in=follow_list)
    posts = posts.order_by("-date").all()

    #Filter posts for objects where user has liked posts (to display in templates on page load)
    post_list = []
    for post in posts:
        post_list.append((post, Like.objects.filter(who_liked=user, what_post=post)))

    #Paginate results
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_obj': page_obj
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
