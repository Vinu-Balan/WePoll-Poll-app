from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

# class Post(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     user = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='post_images')
#     caption = models.TextField()
#     created_at = models.DateTimeField(default=datetime.now)
#     no_of_likes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.user

# class LikePost(models.Model):
#     post_id = models.CharField(max_length=500)
#     username = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    classAName = models.CharField(max_length=100)
    classBName = models.CharField(max_length=100)
    classAno = models.IntegerField(default=0)
    classBno = models.IntegerField(default=0)
    classAPercent = models.IntegerField()
    classBPercent = models.IntegerField()
    # image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.user
class SubmitVote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    poll_id = models.CharField(max_length=500)
    decision = models.BooleanField()
    voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user