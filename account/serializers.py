from rest_framework import serializers
from BackendApi.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = '__all__'
