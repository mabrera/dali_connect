from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField

class User(AbstractUser):
    follows = ManyToManyField("User", blank=True, related_name="followers")
    likes = ManyToManyField("Post", blank=True, related_name="likers")
    year = models.IntegerField(blank=True, null=True)
    picture = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    american_indian_or_alaska_native = models.BooleanField(blank=True, default=False)
    asian = models.BooleanField(blank=True, default=False)
    black_or_african_american = models.BooleanField(blank=True, default=False)
    hispanic_or_latino = models.BooleanField(blank=True, default=False)
    middle_eastern = models.BooleanField(blank=True, default=False)
    native_hawaiian_or_other_pacific_islander = models.BooleanField(blank=True, default=False)
    white = models.BooleanField(blank=True, default=False)
    other = models.BooleanField(blank=True, default=False)
    major = models.TextField(blank=True)
    minor = models.TextField(blank=True)
    modification = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    role = models.TextField(blank=True)
    home = models.TextField(blank=True)
    quote = models.TextField(blank=True)
    favorite_shoe = models.TextField(blank=True)
    favorite_artist = models.TextField(blank=True)
    favorite_color = models.TextField(blank=True)
    phoneType = models.TextField(blank=True)


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster_username": self.poster.get_username(),
            "poster_id": self.poster.pk,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
        }

    def __str__(self):
        return f"{self.poster.username}: {self.content} at {self.timestamp}"
