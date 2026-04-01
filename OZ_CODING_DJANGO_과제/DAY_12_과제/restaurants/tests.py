from http.client import responses

from django.test import TestCase
from restaurants.models import Restaurant
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.name = '테스트유저'
        self.address = '인천광역시 부평구'
        self.contact = '010-0000-0000'

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(
            name = self.name,
            address = self.address,
            contact = self.contact,
        )

        self.assertEqual(restaurant.name, self.name)
        self.assertEqual(restaurant.address, self.address)
        self.assertEqual(restaurant.contact, self.contact)


# > python manage.py test restaurants
# Found 1 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# .
# ----------------------------------------------------------------------
# Ran 1 test in 0.002s
#
# OK
# Destroying test database for alias 'default'...


class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@exmple.com',
            password = 'qwer1234',
            nickname = '테스크유저',
        )

        self.restaurant = Restaurant.objects.create(
            name = '테스트식당',
            address = '인천광역시 부평구',
            contact = '010-0000-0000',
        )

        self.client.force_authenticate(user=self.user)

    def test_restaurant_list_view(self):
        url = reverse('restaurant-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_post_view(self):
        url = reverse('restaurant-list')

        data = {
            'name': '새식당',
            'address': '인천광역시 부평구',
            'contact': '010-0000-0000',
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], '새식당')

    def test_restaurant_detail_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.restaurant.name)

    def test_restaurant_update_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
        data = {
            'name': '수정된식당',
            'address': '수정된주소',
            'contact': '010-0000-0001'
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_delete_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# > python manage.py test restaurants
# Found 6 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# ......
# ----------------------------------------------------------------------
# Ran 6 tests in 0.753s
#
# OK
# Destroying test database for alias 'default'...