from datetime import timedelta

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from analytics.models import ClickEvent
from unittest.mock import patch
from urls.models import ShortURL


User = get_user_model()


class ShortURLAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123"
        )
        self.client.login(username="testuser", password="StrongPass123")
        self.list_create_url = reverse("url-list-create")
        self.short_url = ShortURL.objects.create(
            user=self.user,
            original_url="https://example.com",
            short_code="abc123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_create_short_url_auto_code(self):
        payload = {"original_url": "https://google.com"}
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("short_code", response.data)

    def test_create_short_url_custom_alias(self):
        payload = {"original_url": "https://openai.com", "custom_alias": "myalias"}
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["short_code"], "myalias")

    def test_list_user_urls(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["short_code"], "abc123")

    def test_retrieve_url_detail(self):
        url = reverse("url-detail", args=[self.short_url.short_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["short_code"], "abc123")

    def test_delete_short_url(self):
        url = reverse("url-detail", args=[self.short_url.short_code])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.short_url.refresh_from_db()
        self.assertFalse(self.short_url.is_active)


class ShortURLRedirectTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser2",
            email="redir@test.com",
            password="StrongPass123"
        )
        self.short_url = ShortURL.objects.create(
            user=self.user,
            original_url="https://openai.com",
            short_code="redirect123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.redirect_url = reverse("url-redirect", args=[self.short_url.short_code])

    @patch("analytics.utils.get_client_ip")
    @patch("analytics.utils.get_country_from_ip")
    def test_redirect_creates_click_event(self, mock_get_country, mock_get_ip):
        # Mock IP and country
        mock_get_ip.return_value = "1.2.3.4"
        mock_get_country.return_value = "Testland"

        response = self.client.get(
            self.redirect_url,
            HTTP_USER_AGENT="TestAgent",
            HTTP_REFERER="http://referrer.com"
        )

        # Redirect works
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.short_url.original_url)

        # ClickEvent created
        click = ClickEvent.objects.first()
        self.assertIsNotNone(click)
        self.assertEqual(click.short_url, self.short_url)
        self.assertEqual(click.user_agent, "TestAgent")
        self.assertEqual(click.referrer, "http://referrer.com")
        self.assertEqual(click.country, "Testland")
        self.assertEqual(click.browser, "Other")  # user_agents.parse default
        self.assertEqual(click.os, "Other")

    @patch("analytics.utils.get_client_ip")
    @patch("analytics.utils.get_country_from_ip")
    def test_redirect_expired_url(self, mock_get_country, mock_get_ip):
        expired_url = ShortURL.objects.create(
            user=self.user,
            original_url="https://expired.com",
            short_code="expired",
            expires_at=timezone.now() - timedelta(days=1)
        )
        redirect_url = reverse("url-redirect", args=[expired_url.short_code])

        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 410)
        self.assertEqual(response.json()["detail"], "URL has expired")
