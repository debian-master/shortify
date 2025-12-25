from django.urls import path
from .views import (
    ShortURLListCreateView,
    ShortURLDetailView,
    ShortURLRedirectView
)

urlpatterns = [
    path("", ShortURLListCreateView.as_view(), name="url-list-create"),
    path("<str:short_code>/", ShortURLDetailView.as_view(), name="url-detail"),
    path("redirect/<str:short_code>/", ShortURLRedirectView.as_view(), name="url-redirect")
]
