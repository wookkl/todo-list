from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, CreateTokenView, CreateUserView

app_name = 'users'

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [path(r'token/', CreateTokenView.as_view(), name='token'),
               path(r'join/', CreateUserView.as_view(), name='join')] + router.urls
