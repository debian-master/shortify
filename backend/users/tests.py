from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")  # Make sure your urls.py has this name
        self.profile_url = reverse("profile")    # Make sure your urls.py has this name
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123"
        }
        # refresh = RefreshToken.for_user(self.user)
        # self.access_token = str(refresh.access_token)

        # self.client.credentials(
        #     HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        # )

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertNotIn("password", response.json())  # password should not be returned

    def test_register_user_missing_fields(self):
        """Test registration fails if required fields are missing"""
        data = {"username": "user2"}  # missing password and email
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())

    def test_profile_requires_authentication(self):
        """Test that profile cannot be accessed without login"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated_user(self):
        """Test profile returns correct data for authenticated user"""
        # Create user
        user = User.objects.create_user(**self.user_data)

        # Authenticate using session login (simplest for TestCase)
        self.client.login(username="testuser", password="StrongPass123")

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "testuser")
        self.assertEqual(response.json()["email"], "test@example.com")
        self.assertNotIn("password", response.json())
