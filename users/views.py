from django.contrib.auth import get_user_model

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import authentication, permissions

from users.serializers import UserSerializer, AuthTokenSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    """A simple ViewSet for creating or updating or retieving user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    queryset = get_user_model().objects.all()

    def get_permissions(self):
        if self.action != 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
