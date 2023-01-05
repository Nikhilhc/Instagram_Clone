# Create your models here.
from django.db import models

class User(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    caption = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time_posted = models.DateTimeField()
    hashtags = models.ManyToManyField(Hashtag)

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_liked = models.DateTimeField()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    time_commented = models.DateTimeField()

class Follower(models.Model):
    follower_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    time_followed = models.DateTimeField()

