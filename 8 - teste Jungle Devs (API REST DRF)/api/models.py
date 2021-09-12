from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    name = models.CharField(max_length=150)
    picture = models.URLField(blank=True)


class Article(models.Model):
    user = models.ForeignKey("User", on_delete=CASCADE)
    category = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    firstParagraph = models.TextField()
    body = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)