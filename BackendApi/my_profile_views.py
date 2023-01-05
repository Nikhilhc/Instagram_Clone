from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer,PostSerializer,CommentSerializer,FollowerSerializer
from .models import Post,Like,Follower,User

@api_view(['GET'])
def profile(request, user_id):
    user = User.objects.get(user_id=user_id)
    user_serializer = UserSerializer(user)
    posts = Post.objects.filter(user=user).order_by('-time_posted')
    post_serializer = PostSerializer(posts, many=True)
    followers = Follower.objects.filter(user=user)
    follower_serializer = FollowerSerializer(followers, many=True)
    return Response({
        'user': user_serializer.data,
        'posts': post_serializer.data,
        'following': follower_serializer.data
    })