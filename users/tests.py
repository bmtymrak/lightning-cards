from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@test.com',
            password = 'testpass123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username = 'superadmin',
            email = 'superadmin@test.com',
            password = 'testpass123'
        )

        self.assertEqual(user.username, 'superadmin')
        self.assertEqual(user.email, 'superadmin@test.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)