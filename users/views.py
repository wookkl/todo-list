from django.contrib.auth import get_user_model

from rest_framework.settings import api_settings
from rest_framework.generics import CreateAPIView
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import mixins, GenericViewSet

from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    """A simple ViewSet for updating or retieving user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
