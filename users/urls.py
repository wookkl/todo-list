from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, CreateTokenView

app_name = "users"

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [path(r'token/', CreateTokenView.as_view(),
                    name="token")] + router.urls
