from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_url = models.URLField(default="https://i.imgur.com/0P2wagS.png")


class Follow(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE)
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")


class Post(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


class Like(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes_given")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes_received")