from django.db import models


class ClickEvent(models.Model):
    short_url = models.ForeignKey(
        "urls.ShortURL",
        on_delete=models.CASCADE,
        related_name="clicks"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.TextField(null=True, blank=True)
    user_agent = models.TextField()
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.timestamp}"
