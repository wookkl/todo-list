from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Customized JWTObtainPairView"""
    serializer_class = CustomTokenObtainPairSerializer
