from django.test import TestCase
from django.contrib.auth import get_user_model

from works.models import Work


class ModelTest(TestCase):
    """Model tests"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@naver.com',
            name='test name',
            password='password123@')

    def test_work_str(self):
        """ Test the work string representation """
        work = Work.objects.create(title="today work title",
                                   description="work description",
                                   user=self.user)
        self.assertEqual(work.title, str(work))
