from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterForm, LoginForm
from django.urls import reverse


class ProfileModelTest(TestCase):
    """Test for the Profile model using registration."""

    def setUp(self):
        self.client = Client()

    def test_profile_creation_via_registration(self):
        """Checks if `Profile` is created when a user registers through the form."""
        self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        user = User.objects.get(username='testuser')
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)


class RegisterFormTest(TestCase):
    """Tests for the registration form."""

    def test_register_form_valid(self):
        """Checks if a valid form can create a user."""
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_email(self):
        """Checks if the form rejects a duplicate email."""
        User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',  # already existing email
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LoginFormTest(TestCase):
    """Tests for the login form."""

    def test_login_form_valid(self):
        """Checks if the login form accepts valid data."""
        user = User.objects.create_user(username="testuser", password="testpassword")
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTest(TestCase):
    """Tests for the views (pages)."""

    def setUp(self):
        """Creates a test client and a test user."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_homepage_view(self):
        """Checks if the homepage loads successfully."""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        """Checks if the contact page loads successfully."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_get(self):
        """Checks if the registration page loads successfully (GET request)."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_valid(self):
        """Checks if registration works with valid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        """Checks if the login page loads successfully (GET request)."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid(self):
        """Checks if login works with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # redirect

    def test_login_view_post_invalid(self):
        """Checks if incorrect login returns an error message."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
