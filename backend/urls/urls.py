from django.urls import path
from .views import (
    ShortURLListCreateView,
    ShortURLDetailView,
    ShortURLRedirectView
)

urlpatterns = [
    path("", ShortURLListCreateView.as_view()),
    path("<str:short_code>/", ShortURLDetailView.as_view()),
    path("redirect/<str:short_code>/", ShortURLRedirectView.as_view())
]
