from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import CreateTokenView, CreateUserView, ManageUserView

app_name = 'users'

urlpatterns = [path(r'token/', CreateTokenView.as_view(), name='token'),
               path(r'join/', CreateUserView.as_view(), name='join'),
               path(r'me/', ManageUserView.as_view(), name='me')]
