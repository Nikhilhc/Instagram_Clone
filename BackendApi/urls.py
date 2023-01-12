from django.urls import path, include
from rest_framework import routers
from .my_profile_api import ProfileView, UpdateProfilePictureView,\
    CommentListView,CommentUpdateDelete
from .HomepageApi import HomePageView,CommentUpdateDelete,\
    CommentListView,LikeListCreateView,LikeListDeleteView
from .PostsDetailsApis import PostDetailView

urlpatterns = [
    path('my_profile/<int:user_id>', ProfileView.as_view()),
    path("profile_pic_update/<int:pk>", UpdateProfilePictureView.as_view()),
    path("comments/<int:post_id>", CommentListView.as_view()),
    path("comment_update/<int:pk>", CommentUpdateDelete.as_view()),
    path("like/<int:post_id>", LikeListCreateView.as_view()),
    path("like_delete/<int:post_id>", LikeListDeleteView.as_view()),
    path('homepage/<int:user_id>', HomePageView.as_view()),
    path("posts/<int:post_id>", PostDetailView.as_view()),
]