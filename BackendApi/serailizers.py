from rest_framework import serializers
from .models import User,Post,Like,Hashtag,Comment,Follower

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'name', 'profile_picture')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'image', 'caption', 'location', 'time_posted')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('like_id', 'user', 'post', 'time_liked')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_id', 'user', 'post', 'comment_text', 'time_commented')

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower_id', 'user', 'follower_user', 'time_followed')