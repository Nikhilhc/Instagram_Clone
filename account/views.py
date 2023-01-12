from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from BackendApi.models import User
import boto3

class RegisterViewSet(viewsets.generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        import ipdb;ipdb.set_trace()
        if serializer.is_valid():
            client = boto3.client('cognito-idp')
            response = client.admin_create_user(
                UserPoolId='ap-south-1_lL5m6LsOs',
                Username=request.data.get('username'),
                TemporaryPassword=request.data.get('password'),
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': request.data.get('email')
                    },
                ],
            )
            # access_token = response['AuthenticationResult']['AccessToken']
            # user, _ = CognitoTokenAuthentication().authenticate_credentials(access_token)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)