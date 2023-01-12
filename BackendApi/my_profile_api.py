from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serailizers import UserSerializer, PostSerializer, CommentSerializer, FollowerSerializer
from .models import Post, Like, Follower, User, Comment
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user_id=kwargs['user_id'])
            user_serializer = UserSerializer(user)
            posts = Post.objects.filter(user=user).order_by('-time_posted')
            post_serializer = PostSerializer(posts, many=True)
            followers = Follower.objects.filter(user=user)
            follower_serializer = FollowerSerializer(followers, many=True)
            return Response({
                'user': user_serializer.data,
                'my_posts': post_serializer.data,
                'following_people': follower_serializer.data,
                'following': len(follower_serializer.data),
                'posts_count': len(post_serializer.data),
            })
        except:
            return Response({
                "Details":"User doesnot exists"
            },status=status.HTTP_404_NOT_FOUND)


class UpdateProfilePictureView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(user_id = self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response({
            "UserDetatils": serializer.data
        })

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "UpdatedUser": serializer.data
            })
        return Response({
            "Error": serializer.errors,
        },status=status.HTTP_400_BAD_REQUEST)


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
