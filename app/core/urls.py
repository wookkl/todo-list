from django.urls import path, include

from rest_framework_simplejwt.views import (
    token_refresh,
    token_verify,
)

from .views import CustomTokenObtainPairView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('token/verify/', token_verify, name='token_verify'),
    path('users/', include('users.urls')),
    path('works/', include('works.urls')),
]
