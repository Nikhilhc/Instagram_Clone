import json
import boto3
from django.http import JsonResponse
from functools import wraps

def authenticate_cognito(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extract the token from the request headers
        token = request.headers.get('Authorization')
        # Verify the token with Amazon Cognito
        client = boto3.client('cognito-idp')
        try:
            response = client.get_user(AccessToken=token)
        except client.exceptions.NotAuthorizedException:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        # Attach the user data to the request object
        request.user = response['Username']

        # Call the view function
        return view_func(request, *args, **kwargs)
    return wrapper