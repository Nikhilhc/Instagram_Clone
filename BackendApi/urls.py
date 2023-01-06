from django.urls import path, include
from rest_framework import routers
from .my_profile_api import ProfileView, UpdateProfilePictureView,CommentListView,CommentUpdateDelete

urlpatterns = [
    path('my_profile/<int:user_id>', ProfileView.as_view()),
    path("profile_pic_update/<int:pk>", UpdateProfilePictureView.as_view()),
    path("comments/<int:post_id>", CommentListView.as_view()),
    path("comment_update/<int:pk>", CommentUpdateDelete.as_view()),
]