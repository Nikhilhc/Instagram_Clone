from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serailizers import UserSerializer, PostSerializer, CommentSerializer, FollowerSerializer
from .models import Post, Like, Follower, User, Comment


class ProfileView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(user_id=kwargs['user_id'])
        user_serializer = UserSerializer(user)
        posts = Post.objects.filter(user=user).order_by('-time_posted')
        post_serializer = PostSerializer(posts, many=True)
        followers = Follower.objects.filter(user=user)
        follower_serializer = FollowerSerializer(followers, many=True)

        return Response({
            'user': user_serializer.data,
            'posts': post_serializer.data,
            'following': len(follower_serializer.data),
            'posts_count': len(post_serializer.data)
        })


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)


class CommentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return Comment.objects.filter(pk=comment_id)
