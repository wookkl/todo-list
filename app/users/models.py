from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ User model definition """

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_GOOGLE = "google"

    login_method = models.CharField(
        max_length=10,
        choices=(
            (LOGIN_EMAIL, _("Email")),
            (LOGIN_GITHUB, _("Github")),
            (LOGIN_GOOGLE, _("Google")),
        ),
        default=LOGIN_EMAIL
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()
