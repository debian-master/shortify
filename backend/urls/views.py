from datetime import timezone

from django.shortcuts import get_object_or_404, redirect

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user_agents import parse
from .models import ShortURL
from analytics.models import ClickEvent
from analytics.utils import get_client_ip, get_country_from_ip
from .serializers import ShortURLSerializer, ShortURLCreateSerializer


class ShortURLListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ShortURLCreateSerializer
        return ShortURLSerializer


class ShortURLDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "short_code"
    serializer_class = ShortURLSerializer

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)


class ShortURLRedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_code):
        short_url = get_object_or_404(
            ShortURL,
            short_code=short_code,
            is_active=True,
        )

        # Check expiration
        if short_url.expires_at and short_url.expires_at < timezone.now():
            return Response(
                {"detail": "URL has expired"},
                status=status.HTTP_410_GONE,
            )

        # ---- Analytics ----
        user_agent_str = request.META.get("HTTP_USER_AGENT", "")
        ua = parse(user_agent_str)
        print('*** ',get_client_ip(request))

        ClickEvent.objects.create(
            short_url=short_url,
            referrer=request.META.get("HTTP_REFERER"),
            user_agent=user_agent_str,
            browser=ua.browser.family,
            os=ua.os.family,
            country=get_country_from_ip(get_client_ip(request)),
        )

        return redirect(short_url.original_url)

