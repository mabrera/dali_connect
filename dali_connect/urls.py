from django.urls import path

from . import views

urlpatterns = [

    # Website paths
    path("", views.Index.as_view(), name="index"),
    path("follows", views.Follows.as_view(), name="follows"),
    path("profile/<int:profile_id>", views.Profile.as_view(), name="profile"),
    path("directory", views.DirectoryView.as_view(), name="directory"),
    path("likes", views.Likes.as_view(), name="likes"),
    path("profile_details", views.ProfileDetails.as_view(), name="profile-details"),
    path("profile_picture", views.ProfilePicture.as_view(), name="profile-picture"),

    # Session paths
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
