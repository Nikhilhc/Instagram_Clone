# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures')

class Hashtag(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='posts')
    caption = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time_posted = models.DateTimeField()
    hashtags = models.ManyToManyField(Hashtag)

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    time_liked = models.DateTimeField()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    comment_text = models.CharField(max_length=255)
    time_commented = models.DateTimeField()

class Follower(models.Model):
    follower_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    follower_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    time_followed = models.DateTimeField()

