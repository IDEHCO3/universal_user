from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsOwner
from universal_user.settings import FB
from rest_framework_jwt.settings import api_settings

import json
import requests

class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    authentication_classes = (JSONWebTokenAuthentication, )

class FacebookControl:

    redirect_uri = "http://localhost"
    fb_host = "https://graph.facebook.com/"
    uri_app_access_token = "v2.8/oauth/access_token?client_id={app-id}&redirect_uri={redirect-uri}&client_secret={app-secret}&grant_type=client_credentials"
    uri_inspect_token = "debug_token?input_token={token-to-inspect}&access_token={app-token}"
    uri_user_data = "/v2.8/{user-id}?fields=name,id,email,friends&access_token={app-token}"

    def __init__(self):
        self.app_id = FB['app_id']
        self.app_secret = FB['app_secret']
        self.app_access_token = self.getAppAccessToken()

    def getAppAccessToken(self):
        uri = self.fb_host+self.uri_app_access_token.replace('{app-id}', self.app_id)
        uri = uri.replace('{app-secret}', self.app_secret)
        uri = uri.replace('{redirect-uri}', self.redirect_uri)
        response = requests.get(uri)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data['access_token']
        return None

    def inspectAccessToken(self, userAccessToken):
        if self.app_access_token is not None:
            uri = self.fb_host+self.uri_inspect_token.replace('{token-to-inspect}', userAccessToken)
            uri = uri.replace('{app-token}', self.app_access_token)
            response = requests.get(uri)
            if response.status_code == 200:
                data = json.loads(response.content)
                return data['data']
        return None

    def getUserData(self, user_id):
        if self.app_access_token is not None:
            uri = self.fb_host + self.uri_user_data.replace('{user-id}', user_id)
            uri = uri.replace('{app-token}', self.app_access_token)
            response = requests.get(uri)
            if response.status_code == 200:
                data = json.loads(response.content)
                return data
        return None

    def getUserFB(self, userAccessToken):
        data = self.inspectAccessToken(userAccessToken)
        user_data = None
        if data is not None and 'is_valid' in data and data['is_valid']:
            user_data = self.getUserData(data['user_id'])
        return user_data

class UserFacebook(APIView):

    def __init__(self, *args, **kwargs):
        APIView.__init__(self, *args, **kwargs)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    def getUser(self, userfb):
        try:
            user = User.objects.get(email=userfb['email'])
        except User.DoesNotExist:
            user = None
        return user

    def createUser(self, userfb, userAccessToken):
        if userfb is None:
            return None
        user = User(email=userfb['email'], first_name=userfb['name'], username=userfb['email'], password=userAccessToken[:100])
        user.save()
        return user

    def getToken(self, user):
        token = None
        if user is not None:
            payload = self.jwt_payload_handler(user)
            token = self.jwt_encode_handler(payload)
        return token

    def post(self, request, *args, **kwargs):
        userAccessToken = request.data['accessToken']
        fb = FacebookControl()
        userfb = fb.getUserFB(userAccessToken)
        user = self.getUser(userfb)
        if user is None:
             user = self.createUser(userfb, userAccessToken)
        else:
            user.password = userAccessToken[:100]
            user.save()

        token = self.getToken(user)

        if token is not None:
            return Response({"token": token}, status=200)
        return Response({"error": "It wasn't possible to load user data from facebook"}, status=404)
