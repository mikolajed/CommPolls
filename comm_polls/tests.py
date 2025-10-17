from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_signup_page_loads(self):
        response = self.client.get(reverse('comm_polls:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_works(self):
        login = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login)

    def test_account_settings_requires_login(self):
        response = self.client.get(reverse('comm_polls:account_settings'))
        self.assertRedirects(response, '/accounts/login/?next=/account_settings/')
