"""Tests for the users app."""

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


# Create your tests here.
class LoginTest(TestCase):
    """Unit tests for user login."""

    def setUp(self):
        """Create test user in database (use secure password in case these creds leak into production)."""
        self.client = Client()

        self.test_user = "test1"
        self.test_email = "test1@example.com"
        self.test_pass = User.objects.make_random_password()
        self.user = User.objects.create_user(
            username=self.test_user, email=self.test_email, password=self.test_pass
        )

    def test_login_success(self):
        """Test login with valid (test) credentials is successful."""
        response = self.client.post(
            reverse("user_login"),
            {
                "username": self.test_user,
                "email": self.test_email,
                "password": self.test_pass,
            },
        )

        # Check if login is successful and if redirected to home page as expected
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.assertRedirects(response, reverse("index"))

    def test_login_failure(self):
        """Test that login with invalid credentials is unsuccessful."""
        response = self.client.post(
            reverse("user_login"),
            {
                "username": self.test_user,
                "email": self.test_email,
                "password": "INVALID_PASS",
            },
        )

        # Ensure that login is not successful and that a relevant error message is shown
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertContains(response, "Invalid username or password.")


class RegistrationTest(TestCase):
    """Unit tests for user registration."""

    def setUp(self):
        """Create credentials for existing test user and new user to be created."""
        self.client = Client()

        # Creds for new test user
        self.test_user = "test2"
        self.test_email = "test2@example.com"
        self.test_pass = User.objects.make_random_password()

        # Creds for new test user to be created
        self.test_new_user = "test3"
        self.test_new_email = "test3@example.com"
        self.test_new_pass = User.objects.make_random_password()

        self.user = User.objects.create_user(
            username=self.test_user, email=self.test_email, password=self.test_pass
        )

    def test_registration_success(self):
        """Test user registration works with valid data."""
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.test_new_user,
                "email": self.test_new_email,
                "password1": self.test_new_pass,
                "password2": self.test_new_pass,
            },
        )

        # Check user was created and redirected to home page as expected
        self.assertTrue(User.objects.filter(username=self.test_new_user).exists())
        self.assertRedirects(response, reverse("index"))

    def test_registration_user_exists(self):
        """Test registration with existing username."""
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.test_user,
                "email": self.test_new_email,
                "password1": "TEST_PASS",
                "password2": "TEST_PASS",
            },
        )

        # Check that user that correct error message was provided
        self.assertContains(response, "A user with that username already exists.")

    def test_registration_email_exists(self):
        """Test registration with existing email."""
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.test_new_user,
                "email": self.test_email,
                "password1": "TEST_PASS",
                "password2": "TEST_PASS",
            },
        )

        self.assertContains(response, "Email already exists")

    def test_registration_insecure_password(self):
        """Test registration with insecure password."""
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.test_new_user,
                "email": self.test_new_email,
                "password1": "password123",
                "password2": "password123",
            },
        )

        # Check that user that correct error message was provided
        self.assertContains(response, "This password is too common.")
