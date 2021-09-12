
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("register", views.register, name="register"),

    # API roputes
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow/<int:followed_id>", views.follow, name="follow"),
    path("is_liked/<int:post_id>", views.is_liked, name="is_liked"),
    path("like/<int:post_id>", views.like, name="like"),

]
