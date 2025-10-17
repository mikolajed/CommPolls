from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

class UserIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_signup_flow(self):
        """User can sign up and is redirected to home"""
        response = self.client.post(reverse('comm_polls:signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertContains(response, 'Welcome to CommPolls!')

    def test_login_flow(self):
        """User can log in and is redirected to home"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, testuser!')

    def test_account_settings_requires_login(self):
        """Anonymous user should be redirected to login"""
        response = self.client.get(reverse('comm_polls:account_settings'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_account_settings_update(self):
        """User can update username, email, and upload avatar"""
        self.client.login(username='testuser', password='password123')

        # Create a dummy image file
        avatar_file = SimpleUploadedFile(
            "avatar.png", b"fake-image-content", content_type="image/png"
        )

        response = self.client.post(
            reverse('comm_polls:account_settings'),
            {
                'username': 'updateduser',
                'email': 'updated@example.com',
            },
            files={'avatar': avatar_file},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account details have been updated.')

        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertTrue(hasattr(user.profile, 'avatar'))

    def test_password_change_flow(self):
        """User can change password"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('comm_polls:password_change'),
            {
                'old_password': 'password123',
                'new_password1': 'NewComplex123',
                'new_password2': 'NewComplex123',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password change successful')
