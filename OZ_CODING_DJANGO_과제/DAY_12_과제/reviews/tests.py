from django.test import TestCase

from restaurants.models import Restaurant
from users.models import User
from reviews.models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@exmple.com',
            password = 'qwer1234',
            nickname = '테스트유저',
        )
        self.restaurant = Restaurant.objects.create(
            name = '테스트식당',
            address = '인천광역시 부평구',
            contact = '010-0000-0000',
        )
        self.title = '완전 맛있어요!'
        self.comment = '음식이 맛있었습니다!'

    def test_create_review(self):
        review = Review.objects.create(
            user = self.user,
            restaurant = self.restaurant,
            title = self.title,
            comment = self.comment,
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(review.title, self.title)
        self.assertEqual(review.comment, self.comment)


# > python manage.py test reviews
#
# Found 1 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# .
# ----------------------------------------------------------------------
# Ran 1 test in 0.150s
#
# OK
# Destroying test database for alias 'default'...