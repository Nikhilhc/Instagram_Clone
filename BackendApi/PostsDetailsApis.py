from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serailizers import PostSerializer
from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()

class PostDetailView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Post.objects.get(post_id=post_id)

    def get(self, request, *args, **kwargs):
        try:
            post = self.get_queryset()
            serializer = self.serializer_class(post)
            return Response({
                "post_details": serializer.data
            })
        except:
            return Response({
                "post_error": "No posts. Please contact admin."
            }, status=status.HTTP_400_BAD_REQUEST)