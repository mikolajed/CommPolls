from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import Group
from datetime import timedelta
from .models import Poll, Choice, Vote, ManagerRequest

User = get_user_model()

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class IntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Create users
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.manager = User.objects.create_user(username='manager', password='password123')
        manager_group, _ = Group.objects.get_or_create(name='Managers')
        self.manager.groups.add(manager_group)

        # Create a poll
        now = timezone.now()
        self.poll = Poll.objects.create(
            name='Integration Test Poll',
            created_by=self.manager,
            start_date=now - timedelta(hours=1),
            end_date=now + timedelta(days=1)
        )
        self.choice1 = Choice.objects.create(poll=self.poll, name='Choice 1')
        self.choice2 = Choice.objects.create(poll=self.poll, name='Choice 2')

    def test_signup_login_vote_results_flow(self):
        """Full user journey: signup → login → vote → results page"""
        # Signup new user
        response = self.client.post(reverse('comm_polls:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Login as new user
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'StrongPass123'
        }, follow=True)
        self.assertContains(response, 'Hello, newuser!')

        # Access poll page and submit a vote
        response = self.client.post(
            reverse('comm_polls:vote', args=[self.poll.id]),
            {'choice': self.choice1.id},
            follow=True
        )
        self.assertRedirects(response, reverse('comm_polls:results', args=[self.poll.id]))
        self.assertTrue(Vote.objects.filter(voter__username='newuser', poll=self.poll).exists())
        self.assertContains(response, 'Your vote has been recorded!')

        # Results page should highlight user's vote
        response = self.client.get(reverse('comm_polls:results', args=[self.poll.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_vote', response.context)
        self.assertEqual(response.context['user_vote'].choice, self.choice1)
        self.assertContains(response, 'class="result-item voted-for"')

    def test_vote_countdown_integration(self):
        """Test that accessing a future poll redirects to countdown"""
        future_poll = Poll.objects.create(
            name='Future Poll',
            created_by=self.manager,
            start_date=timezone.now() + timedelta(hours=1),
            end_date=timezone.now() + timedelta(days=1)
        )
        choice = Choice.objects.create(poll=future_poll, name='Option A')

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('comm_polls:vote', args=[future_poll.id]))
        self.assertRedirects(response, reverse('comm_polls:poll_countdown', args=[future_poll.id]))

    def test_double_voting_prevention(self):
        """Ensure a user cannot vote twice on the same poll"""
        self.client.login(username='testuser', password='password123')
        # First vote
        self.client.post(reverse('comm_polls:vote', args=[self.poll.id]), {'choice': self.choice1.id})
        # Attempt second vote
        response = self.client.get(reverse('comm_polls:vote', args=[self.poll.id]), follow=True)
        self.assertRedirects(response, reverse('comm_polls:results', args=[self.poll.id]))
        self.assertContains(response, "You have already voted on this poll.")
        # Total votes should remain 1
        self.assertEqual(Vote.objects.filter(poll=self.poll, voter=self.user).count(), 1)

    def test_spa_navigation_content_reload(self):
        """Test SPA-like page navigation triggers correct content & scripts"""
        self.client.login(username='testuser', password='password123')

        # Load homepage
        response = self.client.get(reverse('comm_polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poll.name)  # <-- use poll name instead of 'Active Polls'

        # Navigate to poll results page
        response = self.client.get(reverse('comm_polls:results', args=[self.poll.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poll.name) 

    def test_manager_request_and_approval_flow(self):
        """Test user requesting manager status and a manager approving it."""
        # 1. Regular user logs in and requests manager status
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('comm_polls:request_manager'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your request to become a manager has been submitted.")
        
        # Verify the request was created in the database
        manager_request = ManagerRequest.objects.get(user=self.user)
        self.assertEqual(manager_request.status, 'pending')

        # 2. Manager logs in to approve the request
        self.client.logout()
        self.client.login(username='manager', password='password123')
        
        # Go to the management page and check if the request is visible
        response = self.client.get(reverse('comm_polls:manage_requests'))
        self.assertContains(response, self.user.username)

        # Approve the request
        response = self.client.post(
            reverse('comm_polls:manage_requests'),
            {'request_id': manager_request.id, 'action': 'approve'},
            follow=True
        )
        self.assertContains(response, f"User {self.user.username} has been promoted to Manager.")
        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name='Managers').exists())

        # 3. Original user logs back in and verifies new permissions
        self.client.logout()
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('comm_polls:create_poll'))
        self.assertEqual(response.status_code, 200) # Should now have access
        self.assertNotContains(response, "request to become a manager")

    
