from rest_framework import serializers
from .models import ShortURL
from .utils import generate_short_code


class ShortURLCreateSerializer(serializers.ModelSerializer):
    custom_alias = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ShortURL
        fields = ("original_url", "custom_alias", "expires_at")

    def create(self, validated_data):
        user = self.context["request"].user
        custom_alias = validated_data.pop("custom_alias", None)

        short_code = custom_alias or generate_short_code()

        return ShortURL.objects.create(
            user=user,
            short_code=short_code,
            **validated_data
        )


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = (
            "original_url",
            "short_code",
            "is_active",
            "expires_at",
            "created_at",
        )
