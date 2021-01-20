from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone, dateformat

from rest_framework.test import APIClient
from rest_framework import status

from works.models import Work

WORKS_URL = reverse("works:work-list")


def detail_url(pk):
    return reverse("works:work-detail", kwargs={'pk': pk})


def today():
    return dateformat.format(timezone.now(), 'Y-m-d')


def sample_work(user, **params):
    """Create sample work object"""
    default = {
        'title': 'work',
        'description': 'go to work',
        'created_at': today()}

    default.update(**params)
    return Work.objects.create(user=user, **default)


class ModelTest(TestCase):
    """Model tests"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@naver.com',
            name='test name',
            password='password123@')

    def test_work_str(self):
        """ Test the work string representation """
        work = Work.objects.create(title='today work title',
                                   description='work description',
                                   created_at=timezone.now(),
                                   user=self.user)
        self.assertEqual(work.title, str(work))


class PublicWorkApiTests(TestCase):
    """Test the works API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required """
        res = self.client.get(WORKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_work_anonymous_user(self):
        """Test creating work object without authentication"""
        payload = {'title': 'test title',
                   'description': 'work description',
                   'created_at': timezone.now()}
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_work_anonymous_user(self):
        """Test retrieving work object without authentication"""
        res = self.client.get(WORKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkApiTest(TestCase):
    """Test the works API (private)"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@naver.com',
            name='test name',
            password='password123@')
        self.client.force_authenticate(user=self.user)

    def test_create_new_work_success(self):
        """Test creating work valid payload is successful"""
        payload = {'title': 'test title',
                   'description': 'test description',
                   'created_at': today()}
        res = self.client.post(WORKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])

    def test_create_new_work_invalid_data(self):
        """ test creating a new work with invalid data"""
        payload = {'title': '',
                   'description': 'test description',
                   'created_at': today(),
                   'user': self.user}

        res = self.client.post(WORKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_work_success(self):
        """Test retrieving work """
        sample_work(self.user, **{'title': 'title1'})
        sample_work(self.user, **{'title': 'title2'})

        res = self.client.get(WORKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_recipes_limited_to_user(self):
        """ Test retrieving works for user """
        user2 = get_user_model().objects.create_user(email='testst@naver.com',
                                                     name='teest name',
                                                     password='password123')
        sample_work(user2, **{'title': 'title1'})
        sample_work(user2, **{'title': 'title2'})

        sample_work(self.user, **{'title': 'user1 work'})

        res = self.client.get(WORKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_partial_update_work(self):
        """Test updating a work with patch """
        work = sample_work(user=self.user)
        payload = {'title': 'changed title', 'description': 'new description'}
        url = detail_url(self.user.pk)

        res = self.client.patch(url, payload)
        work.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], work.title)
        self.assertEqual(payload['description'], work.description)

    def test_full_update_work(self):
        """Test updating a work with put"""
        work = sample_work(user=self.user)
        url = detail_url(self.user.pk)
        new_date = datetime.strptime('10-27-2020', '%m-%d-%Y').date()
        payload = {'title': 'changed title',
                   'description': 'new description',
                   'created_at': new_date}

        res = self.client.put(url, payload)
        work.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(work.title, payload['title'])
        self.assertEqual(work.description, payload['description'])
        self.assertEqual(work.created_at, payload['created_at'])
