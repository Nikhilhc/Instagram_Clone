from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serailizers import UserSerializer, PostSerializer,\
    CommentSerializer, FollowerSerializer, LikeSerializer
from .models import Post, Like, Follower, User, Comment
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class HomePageView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(user_id=kwargs['user_id'])
        user_serializer = UserSerializer(user)
        posts = Post.objects.filter(user=user).order_by('-time_posted')
        post_serializer = PostSerializer(posts, many=True)
        followers = Follower.objects.filter(user=user)
        follower_serializer = FollowerSerializer(followers, many=True)
        follower_ids = Follower.objects.filter(user=user).only("follower_user_id").values_list("follower_user_id",
                                                                                               flat=False)
        all_post_inc_followers = Post.objects.filter(user__in=follower_ids)
        all_post_serializer = PostSerializer(all_post_inc_followers, many=True)
        return Response({
            'user': user_serializer.data,
            'my_posts': post_serializer.data,
            'following_people': follower_serializer.data,
            'following': len(follower_serializer.data),
            'posts_count': len(post_serializer.data),
            "all_posts_with_follower": all_post_serializer.data
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


class LikeListCreateView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)

    def get(self, request, *args, **kwargs):
        try:
            like = self.get_queryset()
            serializer = LikeSerializer(like, many=True)
            return Response({
                "like_post": serializer.data
            })
        except:
            return Response({
                "result": "Post not liked."
            }, status=status.HTTP_200_OK)

class LikeListDeleteView(generics.DestroyAPIView):
    serializer_class = LikeSerializer

    def get_object(self):
        post_id = self.kwargs['post_id']
        # Change once the authentication module is done
        user = User.objects.get(user_id=self.request.user.id)
        return Like.objects.get(Q(post_id=post_id)&Q(user=user))

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({
                "result": "Unliked the post"
            },status=status.HTTP_200_OK)
        except:
            return Response({
                "result": "Post not liked."
            }, status=status.HTTP_200_OK)

