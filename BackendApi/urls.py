from django.urls import path, include
from rest_framework import routers
from .my_profile_views import profile



urlpatterns = [
    path('my_profile/<int:user_id>', profile),
]