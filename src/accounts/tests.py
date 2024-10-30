from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import messages
from accounts.models.custom_user import CustomUser


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("register")
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
            "code_word": "secret",
        }

        self.invalid_data_password_mismatch = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123",
            "password2": "DifferentPassword",
            "code_word": "secret",
        }
        self.invalid_data_not_unique_email = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        }
        # Create user for testing not unique email
        CustomUser.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password="Testpassword123",
        )

    def test_user_registration(self):
        """Test success registration user"""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.valid_data["email"]).exists())

    def test_registration_with_mismatched_passwords(self):
        """Test registration with mismatched passwords"""
        response = self.client.post(self.url, self.invalid_data_password_mismatch, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn(
            str(messages.PASSWORDS_DONT_MATCH_ERROR_MESSAGE),
            response.data["non_field_errors"][0],
        )

    def test_registration_with_not_unique_email(self):
        """Test registration with not unique email"""
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "existinguser@example.com",
                "password1": "Testpassword123",
                "password2": "Testpassword123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(_(messages.NOT_UNIQUE_EMAIL_ERROR_MESSAGE), response.data["email"])

    def test_registration_with_code_word(self):
        """Test registration with code word"""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = CustomUser.objects.get(email=self.valid_data["email"])
        self.assertEqual(user.code_word, self.valid_data["code_word"])

    def test_registration_without_code_word(self):
        """Test registration without code word"""
        data_without_code_word = self.valid_data.copy()
        data_without_code_word.pop("code_word")
        response = self.client.post(self.url, data_without_code_word, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = CustomUser.objects.get(email=self.valid_data["email"])
        self.assertEqual(user.code_word, "")


class CustomTokenObtainPairViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("login")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Testpassword123",
        )

    def test_successful_login(self):
        """Test successful login and token generation."""
        response = self.client.post(
            self.url,
            {"email": "testuser@example.com", "password": "Testpassword123"},
            format="json",
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            self.url,
            {"email": "testuser@example.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Testpassword123",
        )
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_successful_token_refresh(self):
        """Test successful token refresh."""
        url = reverse("refresh")
        response = self.client.post(url, {"refresh": self.refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_with_invalid_token(self):
        """Test token refresh with invalid token."""
        url = reverse("refresh")
        response = self.client.post(url, {"refresh": "invalidtoken"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomTokenBlacklistViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Testpassword123",
        )
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_successful_token_blacklist(self):
        """Test successful token blacklisting on logout."""
        url = reverse("logout")
        response = self.client.post(url, {"refresh": self.refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("refresh")
        response = self.client.post(url, {"refresh": self.refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_invalid_token(self):
        """Test logout with invalid token."""
        url = reverse("logout")
        response = self.client.post(url, {"refresh": "invalidtoken"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
