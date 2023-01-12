from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import authentication
from jose import jwt
import jose
import json
from rest_framework import exceptions
import boto3
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from jwcrypto import jwk

def get_public_key(access_token):
    headers = jwt.get_unverified_headers(access_token)
    kid = headers.get("kid")
    #get jwks from cognito
    r = requests.get("https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_lL5m6LsOs/.well-known/jwks.json")
    jwks = r.json()
    key = None
    for key in jwks["keys"]:
        if key["kid"] == kid:
            key = jwk.JWK.from_json(json.dumps(key))
            break
    return key


class CognitoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        client = boto3.client('cognito-idp')
        try:
            # Call the Cognito service to authenticate the user
            response = client.admin_initiate_auth(
                UserPoolId="ap-south-1_lL5m6LsOs",
                ClientId='3bh8f2gsr5p8e3tps9fgfbktc2',
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            # Extract the user's email address
            if 'AuthenticationResult' in response:
                access_token = response['AuthenticationResult']['AccessToken']
                refresh_token = response['AuthenticationResult']['RefreshToken']
                request.COOKIES['access_token'] = access_token
                request.COOKIES['refresh_token'] = refresh_token
                try:
                    key = get_public_key(access_token)
                except:
                    msg = 'Invalid token'
                    raise exceptions.AuthenticationFailed(msg)
                username = jwt.decode(access_token, key, algorithms='RS256')['username']
            # Try to find an existing user with this email address
            user = User.objects.get(username=username)
        except Exception as e:
            # if the authentication fails, return None
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class CognitoTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        if not access_token:
            return None

        parts = access_token.split()
        if parts[0].lower() != 'bearer':
            msg = 'Invalid authentication header.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(parts) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(parts) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)
        access_token = parts[1]
        try:
            key = get_public_key(access_token)
        except:
            msg = 'Invalid token'
            raise exceptions.AuthenticationFailed(msg)
        try:
            username = jwt.decode(access_token, key, algorithms='RS256')['username']
            client = boto3.client('cognito-idp')
        except:
            msg = 'Invalid token'
            raise exceptions.AuthenticationFailed(msg)
        try:
            # Use the 'admin_initiate_auth' or 'initiate_auth' method to authenticate the user and validate the token
            resp = client.get_user(AccessToken=access_token)
            print(resp)
        except client.exceptions.NotAuthorizedException as e:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        # If authentication was successful, return the user
        return (username, None)

