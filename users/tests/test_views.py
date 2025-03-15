from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Role, Permission

class UserViewTests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Admin")
        self.permission = Permission.objects.create(name="Can View")
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User",
            company="Test Company",
            phone_number="1234567890",
            country="Test Country",
            status="Active"
        )
        self.user.roles.add(self.role)
        self.user.permissions.add(self.permission)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            "email": "newuser@example.com",
            "password": "password123",
            "name": "New User",
            "company": "New Company",
            "phone_number": "0987654321",
            "country": "New Country",
            "status": "Active",
            "roles": [self.role.id],
            "permissions": [self.permission.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_statistics(self):
        url = reverse('user_statistics')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_users'], 1)
        self.assertEqual(response.data['active_users'], 1)
        self.assertEqual(response.data['inactive_users'], 0)

class RoleViewTests(APITestCase):
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
        self.client.force_authenticate(user=self.user)

    def test_create_role(self):
        url = reverse('role-list')
        data = {"name": "Manager"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_roles(self):
        url = reverse('role-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PermissionViewTests(APITestCase):
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
        self.client.force_authenticate(user=self.user)

    def test_create_permission(self):
        url = reverse('permission-list')
        data = {"name": "Can Edit"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_permissions(self):
        url = reverse('permission-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
