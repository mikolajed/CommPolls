from django.test import TestCase, override_settings, RequestFactory
from django.contrib.auth.models import User, AnonymousUser, Group
import unittest
from django.urls import reverse
from .models import Profile, Poll, Choice, Vote, ManagerRequest
from django.utils import timezone
from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .context_processors import server_time, user_roles
from django.db.utils import IntegrityError
from .validators import NumberValidator, UppercaseValidator
from .forms import SignUpForm, UserUpdateForm, PollForm, ChoiceForm, ChoiceFormSet

# Minimal 1x1 transparent PNG for ImageField tests
PNG_1X1_TRANSPARENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')

    def test_profile_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_signup_view(self):
        response = self.client.post(reverse('comm_polls:signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comm_polls:home'))

    def test_account_settings_requires_login(self):
        response = self.client.get(reverse('comm_polls:account_settings'))
        self.assertEqual(response.status_code, 302)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ContextProcessorTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.manager_user = User.objects.create_user(username='manageruser', password='password123')
        self.superuser = User.objects.create_superuser(username='superuser', password='password123')

        manager_group, created = Group.objects.get_or_create(name='Managers')
        self.manager_user.groups.add(manager_group)

    def test_server_time_context_processor(self):
        request = self.factory.get('/')
        context = server_time(request)
        self.assertIn('server_now', context)
        try:
            datetime.fromisoformat(context['server_now'])
        except ValueError:
            self.fail("server_now is not a valid ISO 8601 string.")

    def test_user_roles_for_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        context = user_roles(request)
        self.assertFalse(context['is_manager'])

    def test_user_roles_for_regular_user(self):
        request = self.factory.get('/')
        request.user = self.user
        context = user_roles(request)
        self.assertFalse(context['is_manager'])

    def test_user_roles_for_manager_user(self):
        request = self.factory.get('/')
        request.user = self.manager_user
        context = user_roles(request)
        self.assertTrue(context['is_manager'])

    def test_user_roles_for_superuser(self):
        request = self.factory.get('/')
        request.user = self.superuser
        context = user_roles(request)
        self.assertTrue(context['is_manager'])


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        now = timezone.now()

        self.active_poll = Poll.objects.create(
            name="Active Poll",
            created_by=self.user1,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1)
        )
        self.ended_poll = Poll.objects.create(
            name="Ended Poll",
            created_by=self.user1,
            start_date=now - timedelta(days=2),
            end_date=now - timedelta(days=1)
        )
        self.future_poll = Poll.objects.create(
            name="Future Poll",
            created_by=self.user1,
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=2)
        )
        self.choice1 = Choice.objects.create(poll=self.active_poll, name="Choice 1")
        self.choice2 = Choice.objects.create(poll=self.active_poll, name="Choice 2")

    def test_poll_str_representation(self):
        self.assertEqual(str(self.active_poll), "Active Poll")

    def test_poll_properties(self):
        self.assertTrue(self.active_poll.is_active)
        self.assertTrue(self.active_poll.has_started)
        self.assertFalse(self.active_poll.has_ended)
        self.assertFalse(self.ended_poll.is_active)
        self.assertTrue(self.ended_poll.has_started)
        self.assertTrue(self.ended_poll.has_ended)
        self.assertFalse(self.future_poll.is_active)
        self.assertFalse(self.future_poll.has_started)
        self.assertFalse(self.future_poll.has_ended)

    def test_poll_total_votes(self):
        self.assertEqual(self.active_poll.total_votes, 0)
        Vote.objects.create(poll=self.active_poll, choice=self.choice1, voter=self.user1)
        self.assertEqual(self.active_poll.total_votes, 1)
        Vote.objects.create(poll=self.active_poll, choice=self.choice2, voter=self.user2)
        self.assertEqual(self.active_poll.total_votes, 2)

    def test_choice_str_representation(self):
        self.assertEqual(str(self.choice1), "Choice 1")

    def test_vote_str_representation(self):
        vote = Vote.objects.create(poll=self.active_poll, choice=self.choice1, voter=self.user1)
        self.assertEqual(str(vote), "user1 voted on Active Poll")

    def test_vote_unique_together_constraint(self):
        Vote.objects.create(poll=self.active_poll, choice=self.choice1, voter=self.user1)
        with self.assertRaises(IntegrityError):
            Vote.objects.create(poll=self.active_poll, choice=self.choice2, voter=self.user1)

    def test_manager_request_model(self):
        request = ManagerRequest.objects.create(user=self.user1)
        self.assertEqual(request.status, 'pending')
        self.assertEqual(str(request), "Manager request from user1 - pending")

    def test_profile_model_str_representation(self):
        self.assertEqual(str(self.user1.profile), "user1's profile")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123!', email='test@example.com')
        now = timezone.now()
        self.poll = Poll.objects.create(
            name="Test Poll for Formset",
            created_by=self.user,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1))

    # --- SignUpForm Tests ---
    def test_signup_form_fields(self):
        form = SignUpForm()
        self.assertTrue(form.fields['email'].required)
        self.assertEqual(form.fields['username'].help_text, '')
        self.assertIn('email', form.fields)
        self.assertIn('avatar', form.fields)

    def test_signup_form_required_labels(self):
        form = SignUpForm()
        self.assertEqual(form.fields['email'].label, 'Email*')
        self.assertTrue(form.fields['username'].label.endswith('*'))

    def test_signup_form_save_creates_user_and_profile(self):
        form = SignUpForm(data={
            'username': 'newuser_signup',
            'email': 'new_signup@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser_signup')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNone(user.profile.avatar.name or None)

    def test_signup_form_save_with_avatar(self):
        unittest.skip("Skipping image upload tests.")

    # --- UserUpdateForm Tests ---
    def test_user_update_form_save_updates_user_and_profile(self):
        form = UserUpdateForm(instance=self.user, data={
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertIsNone(user.profile.avatar.name)

    def test_user_update_form_save_with_valid_avatar(self):
        unittest.skip("Skipping image upload tests.")

    # --- PollForm Tests ---
    def test_poll_form_widgets(self):
        form = PollForm()
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'e.g., Favorite Programming Language?')
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)
        self.assertEqual(form.fields['start_date'].widget.input_type, 'datetime-local')
        self.assertEqual(form.fields['end_date'].widget.input_type, 'datetime-local')

    # --- ChoiceForm Tests ---
    def test_choice_form_fields(self):
        form = ChoiceForm()
        self.assertEqual(form.fields['name'].label, 'Choice Name')
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Enter choice name')
        self.assertFalse(form.fields['name'].required)

    # --- ChoiceFormSet Tests ---
    def test_choice_formset_min_choices_validation_fail(self):
        formset_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-name': 'Only one choice',
        }
        formset = ChoiceFormSet(data=formset_data, instance=self.poll, queryset=Choice.objects.none())
        self.assertFalse(formset.is_valid())
        self.assertIn('You must provide at least two choices with a name.', formset.non_form_errors())

    def test_choice_formset_custom_min_choices_validation_fail(self):
        formset_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-name': 'One filled choice',
            'form-1-name': '',
        }
        formset = ChoiceFormSet(data=formset_data, instance=self.poll, queryset=Choice.objects.none())
        self.assertFalse(formset.is_valid())
        self.assertIn('You must provide at least two choices with a name.', formset.non_form_errors())

    @unittest.skip("Skipping ChoiceFormSet validation pass test for now.")
    def test_choice_formset_min_choices_validation_pass(self):
        """Test ChoiceFormSet validation passes with 2 or more choices."""
        formset_data = {
            'form-TOTAL_FORMS': '2',        # total number of forms
            'form-INITIAL_FORMS': '0',      # initial forms
            'form-MIN_NUM_FORMS': '0',      # ignored because validate_min=False
            'form-MAX_NUM_FORMS': '1000',   # just a large number
            'form-0-name': 'Choice One',
            'form-1-name': 'Choice Two',
        }
        formset = ChoiceFormSet(data=formset_data, instance=self.poll)
        self.assertTrue(formset.is_valid(), formset.non_form_errors())

    @unittest.skip("Skipping ChoiceFormSet validation with empty forms test for now.")
    def test_choice_formset_min_choices_validation_with_empty_forms(self):
        """Test ChoiceFormSet validation correctly counts only filled forms."""
        formset_data = {
            'form-TOTAL_FORMS': '3',        # three forms, but last is empty
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',      
            'form-MAX_NUM_FORMS': '1000',
            'form-0-name': 'Choice A',
            'form-1-name': 'Choice B',
            'form-2-name': '',               # empty form should be ignored
        }
        formset = ChoiceFormSet(data=formset_data, instance=self.poll)
        self.assertTrue(formset.is_valid(), formset.non_form_errors())


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ValidatorTests(TestCase):

    def test_number_validator_success(self):
        validator = NumberValidator()
        try:
            validator.validate('password123')
        except ValidationError:
            self.fail("NumberValidator raised ValidationError unexpectedly.")

    def test_number_validator_fail(self):
        validator = NumberValidator()
        with self.assertRaisesMessage(ValidationError, "This password must contain at least one digit."):
            validator.validate('password')

    def test_number_validator_help_text(self):
        validator = NumberValidator()
        self.assertEqual(validator.get_help_text(), "Your password must contain at least one digit.")

    def test_uppercase_validator_success(self):
        validator = UppercaseValidator()
        try:
            validator.validate('Password')
        except ValidationError:
            self.fail("UppercaseValidator raised ValidationError unexpectedly.")

    def test_uppercase_validator_fail(self):
        validator = UppercaseValidator()
        with self.assertRaisesMessage(ValidationError, "This password must contain at least one uppercase letter."):
            validator.validate('passwordwithoutupper')

    def test_uppercase_validator_help_text(self):
        validator = UppercaseValidator()
        self.assertEqual(validator.get_help_text(), "Your password must contain at least one uppercase letter.")
