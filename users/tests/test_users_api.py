from django.test import TestCase
from django.core.validators import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from users import models


CREATE_USER_URL = reverse("users:user-list")
TOKEN_URL = reverse("users:token")


def get_retrieve_user_url(pk=0):
    return reverse("users:user-detail", kwargs={'pk': pk})


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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


class PublicUserApiTest(TestCase):

    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_creat_valid_user_success(self):
        """Test creating user valid payload is successful"""
        payload = {
            'email': 'test@naver.com',
            'name': 'test name',
            'password': 'password123@'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'test@naver.com',
            'name': 'test name',
            'password': 'password123@'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {
            'email': 'test@navermcom',
            'name': 'test name',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@naver.com',
                   'password': 'testpassword123@',
                   'name': 'test name'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@naver.com',
                    password='password123@',
                    name='test name')

        payload = {'email': 'test@naver.com', 'password': 'wrongpw123@'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_not_user(self):
        """Test that token is note created if user doesn't exists"""
        payload = {'email': 'test@naver.com', 'password': 'passwor1d123@'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'test', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        user = create_user(email='test@naver.com',
                           password='password123',
                           name='test name')
        res = self.client.get(get_retrieve_user_url(user.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the users API (private)"""

    def setUp(self):
        self.user = create_user(email='test@naver.com',
                                password='password123',
                                name='test name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(get_retrieve_user_url(self.user.pk))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {'name': self.user.name, 'email': self.user.email}
        )

    def test_post_retrieve_not_allowed(self):
        """Test that POST is not allowed on the retrieve url"""
        res = self.client.post(get_retrieve_user_url(self.user.pk), {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'changed name', 'password': 'password121131@'}

        res = self.client.patch(get_retrieve_user_url(self.user.pk), payload)
        self.user.refresh_from_db()
        self.assertEqual(res.data['name'], payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
