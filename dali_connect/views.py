from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.shortcuts import render
import json

from .models import User, Post

#-----------------------------------------------------------------------------#
#------------------------------- Website Views -------------------------------#
#-----------------------------------------------------------------------------#

# Site-wide feed
class Index(View):

    def get(self, request):
        # Get all posts, order them from newest to oldest
        posts = Post.objects.all().order_by("-timestamp").all()
        post_dict = []
        # If logged in, figure out which posts are liked by user and which aren't
        for post in posts:
            if request.user.is_authenticated:
                if post in request.user.likes.all():
                    post_dict.append((post, "Unlike"))
                else:
                    post_dict.append((post, "Like"))
            else:
                post_dict.append((post, None))
        # Pagination
        paginator = Paginator(post_dict, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {
            'profile': None,
            'page_obj': page_obj,
            'is_authenticated': request.user.is_authenticated,
            'is_profile': False,
            'data': {
                'view': 'index',
                'is_authenticated': request.user.is_authenticated
            }
        })

    def post(self, request):
        new_post = Post(
            poster = request.user,
            content = request.POST['content']
        )
        new_post.save()
        return HttpResponseRedirect(reverse("index"))


# Followed users feed (only accessible if logged in)
class Follows(View):
    
    def get(self, request):
        # Get all users followed by session user
        follows = User.objects.get(pk=request.user.pk).follows.all()
        # Get their posts, order them from newest to oldest
        posts = Post.objects.filter(poster__in=follows).order_by("-timestamp").all()
        post_dict = []
        # Figure out which posts are liked by user and which aren't
        for post in posts:
            if request.user.is_authenticated:
                if post in request.user.likes.all():
                    post_dict.append((post, "Unlike"))
                else:
                    post_dict.append((post, "Like"))
            else:
                post_dict.append((post, None))
        # Pagination
        paginator = Paginator(post_dict, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {
            'profile': User.objects.get(pk=request.user.pk),
            'page_obj': page_obj,
            'is_authenticated': request.user.is_authenticated,
            'is_profile': False,
            'data': {
                'view': 'follows',
                'is_authenticated': request.user.is_authenticated
            }
        })
    
    def post(self, request):
        new_post = Post(
            poster = request.user,
            content = request.POST['content']
        )
        new_post.save()
        return HttpResponseRedirect(reverse("follows"))


@method_decorator(csrf_exempt, name='dispatch')
class Profile(View):

    def get(self, request, profile_id):
        # Get all posts made by user whose profile this is, order them from newest to oldest
        posts = User.objects.get(pk=profile_id).posts.all().order_by("-timestamp").all()
        post_dict = []
        # If logged in, figure out which posts are liked by user and which aren't
        for post in posts:
            if request.user.is_authenticated:
                if post in request.user.likes.all():
                    post_dict.append((post, "Unlike"))
                else:
                    post_dict.append((post, "Like"))
            else:
                post_dict.append((post, None))
        # Pagination
        paginator = Paginator(post_dict, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {
            'profile': User.objects.get(pk=profile_id),
            'page_obj': page_obj,
            'is_authenticated': request.user.is_authenticated,
            'is_profile': True,
            'data': {
                'view': 'profile',
                'user_id': request.user.pk,
                'profile_id': profile_id,
                'is_following': request.user.is_authenticated and (User.objects.get(pk=profile_id) in request.user.follows.all()),
                'is_authenticated': request.user.is_authenticated
            }
        })

    def post(self, request, profile_id):
        new_post = Post(
            poster = request.user,
            content = request.POST['content']
        )
        new_post.save()
        return HttpResponseRedirect(reverse("profile", args=(profile_id,)))

    # For adding this profile's user to session user's follows
    def put(self, request, profile_id):
        data = json.loads(request.body)
        if data.get("follow") == True:
            request.user.follows.add(User.objects.get(pk=profile_id))
        else:
            request.user.follows.remove(User.objects.get(pk=profile_id))
        return HttpResponse(status=204)



class DirectoryView(View):

    def get(self, request):
        # Get all users
        users = User.objects.all()
        return render(request, 'index.html', {
            'users': users,
            'data': {
                'view': 'directory',
                'is_authenticated': request.user.is_authenticated
            },
        })


@method_decorator(csrf_exempt, name='dispatch')
class Likes(View):

    def get(self, request):
        likes = []
        for post in request.user.likes.all():
            likes.append(post.id)
        return JsonResponse(json.dumps(likes), safe=False)

    def put(self, request):
        data = json.loads(request.body)
        if data.get("like") == True:
            request.user.likes.add(Post.objects.get(pk=data.get("post_id")))
        else:
            request.user.likes.remove(Post.objects.get(pk=data.get("post_id")))
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetails(View):

    # For updating profile details
    # Read in form data and update info in database
    def post(self, request):
        user = request.user
        user.gender = request.POST["gender"]
        user.birthday = request.POST["birthday"]
        user.home = request.POST["home"]
        user.american_indian_or_alaska_native = False
        user.asian = False
        user.black_or_african_american = False
        user.hispanic_or_latino = False
        user.middle_eastern = False
        user.native_hawaiian_or_other_pacific_islander = False
        user.white = False
        if "american_indian_or_alaska_native" in request.POST:
            user.american_indian_or_alaska_native = True
        if "asian" in request.POST:
            user.asian = True
        if "black_or_african_american" in request.POST:
            user.black_or_african_american = True
        if "hispanic_or_latino" in request.POST:
            user.hispanic_or_latino = True
        if "middle_eastern" in request.POST:
            user.middle_eastern = True
        if "native_hawaiian_or_other_pacific_islander" in request.POST:
            user.native_hawaiian_or_other_pacific_islander = True
        if "white" in request.POST:
            user.white = True
        user.major = request.POST["major"]
        user.modification = request.POST["modification"]
        user.minor = request.POST["minor"]
        user.quote = request.POST["quote"]
        user.favorite_shoe = request.POST["favorite_shoe"]
        user.favorite_artist = request.POST["favorite_artist"]
        user.favorite_color = request.POST["favorite_color"]
        user.phoneType = request.POST["phoneType"]
        user.save()
        return HttpResponseRedirect(reverse("profile", args=(user.pk,)))


@method_decorator(csrf_exempt, name='dispatch')
class ProfilePicture(View):

    def post(self, request):
        user = request.user
        user.picture = request.POST["picture"]
        user.save()
        return HttpResponseRedirect(reverse("profile", args=(user.pk,)))


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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        year = request.POST["year"]
        email = request.POST["email"]
        role = request.POST["role"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.year = year
            user.role = role
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


#-----------------------------------------------------------------------------#
#--------------------------------- API Views ---------------------------------#
#-----------------------------------------------------------------------------#
