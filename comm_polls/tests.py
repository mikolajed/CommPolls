from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from django.utils import timezone

class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')

    def test_profile_created(self):
        """Check that a Profile is automatically created for a new user"""
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_signup_view(self):
        """Signup page should create a user and redirect to home"""
        response = self.client.post(reverse('comm_polls:signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Login page works for correct credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comm_polls:home'))

    def test_account_settings_requires_login(self):
        """Account settings page should require login"""
        response = self.client.get(reverse('comm_polls:account_settings'))
        self.assertEqual(response.status_code, 302)  # Redirect to login