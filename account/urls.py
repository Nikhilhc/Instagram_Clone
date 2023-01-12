from django.urls import path, include
from rest_framework import routers
from .views import RegisterViewSet


urlpatterns = [
    path('register/', RegisterViewSet.as_view()),
]