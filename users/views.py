from django.contrib.auth import get_user_model

from rest_framework.settings import api_settings
from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import mixins, GenericViewSet

from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class ManageUserView(generics.RetrieveUpdateAPIView):
    """A simple ViewSet for updating or retieving user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """ Retrieve and return authentication user """
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
