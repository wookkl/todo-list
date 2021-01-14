from django.test import TestCase
from django.core.validators import ValidationError, validate_email
from users import models


class ModelTests(TestCase):
    """ Model tests """

    def test_create_new_user_successfully(self):
        """ Test creating a new user """

        email = "test@naver.com"
        password = "testpassword123@"
        name = "test name"
        user = models.User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_new_user_invalid_email(self):
        """ test creating a new user with invalid email """
        with self.assertRaises(ValidationError):
            models.User.objects.create_user(
                name="test name",
                email=None,
                password="password123@"
            )

    def test_create_new_superuser_successfully(self):
        """ Test creating a new superuser """
        email = "superuser@naver.com"
        password = "superuserpassword123@"
        name = "super user"
        superuser = models.User.objects.create_superuser(
            email=email, name=name, password=password)

        self.assertTrue(superuser.is_superuser)
