from django.test import TestCase
from users.models import User, Role, Permission

class UserModelTests(TestCase):
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

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.permissions.count(), 1)

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email="superuser@example.com",
            password="password123"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
