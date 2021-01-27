from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions

from core.authentication import CustomJWTAuthentication
from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class ManageUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    authentication_classes = [CustomJWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """ Retrieve and return authentication user """
        return self.request.user
