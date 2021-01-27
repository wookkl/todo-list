from django.urls import path

from users.views import CreateUserView, ManageUserView

app_name = 'users'

urlpatterns = [path(r'join/', CreateUserView.as_view(), name='join'),
               path(r'me/', ManageUserView.as_view(), name='me'), ]
