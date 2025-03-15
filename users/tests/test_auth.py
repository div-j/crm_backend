from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User",
            company="Test Company",
            phone_number="1234567890",
            country="Test Country",
            status="Active"
        )

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        url = reverse('token_refresh')
        data = {
            "refresh": refresh_token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
