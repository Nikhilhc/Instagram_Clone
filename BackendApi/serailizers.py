from rest_framework import serializers
from .models import User,Post,Like,Hashtag,Comment,Follower

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255,required=False)
    confirm_password = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = '__all__'

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