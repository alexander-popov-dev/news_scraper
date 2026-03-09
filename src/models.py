from django.db import models
from django.db.models import Q

from src.core.enums import BrowserProvider, ScrapingDataType, SessionStatus


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Session(BaseModel):
    status = models.CharField(
        max_length=20, choices=[(s.value, s.name) for s in SessionStatus], db_index=True
    )
    scraping_type = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in ScrapingDataType],
        db_index=True,
    )
    error_msg = models.TextField(null=True, blank=True)
    traceback_msg = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_saved = models.PositiveIntegerField(default=0)
    retries = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "session"
        indexes = [
            models.Index(fields=["scraping_type"]),
            models.Index(fields=["status", "created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="session_scraping_type_valid",
                condition=Q(
                    scraping_type__in=[
                        scraping_type.value for scraping_type in ScrapingDataType
                    ]
                ),
            ),
            models.CheckConstraint(
                name="session_status_valid",
                condition=Q(status__in=[status.value for status in SessionStatus]),
            ),
        ]

    def __str__(self):
        return f"Session: {self.id}_{self.scraping_type}_{self.status}"


class Site(BaseModel):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    package = models.CharField(max_length=255)
    proxy = models.TextField(null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "site"

    def __str__(self):
        return self.name


class RawResponseData(BaseModel):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="raw_responses", db_index=True
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="raw_responses", db_index=True
    )
    url = models.URLField()
    scraping_type = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in ScrapingDataType],
        db_index=True,
    )
    request_data = models.JSONField()
    response_text = models.TextField()

    class Meta:
        db_table = "raw_response_data"
        indexes = [
            models.Index(fields=["site", "scraping_type"]),
            models.Index(fields=["session", "url"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="raw_response_data_scraping_type_valid",
                condition=Q(
                    scraping_type__in=[
                        scraping_type.value for scraping_type in ScrapingDataType
                    ]
                ),
            )
        ]

    def __str__(self):
        return f"{self.scraping_type}_{self.url}"


class Article(BaseModel):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="articles", db_index=True
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="articles", db_index=True
    )
    url = models.URLField(max_length=5000)
    title = models.CharField(max_length=1000)
    subtitle = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    scraping_type = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in ScrapingDataType],
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "article"
        indexes = [
            models.Index(fields=["site", "scraping_type"]),
            models.Index(fields=["published_at"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["url"], name="unique_article_url"),
            models.CheckConstraint(
                name="article_scraping_type_valid",
                condition=Q(
                    scraping_type__in=[
                        scraping_type.value for scraping_type in ScrapingDataType
                    ]
                ),
            ),
        ]

    def __str__(self):
        return self.title


class BrowserProfile(BaseModel):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="browser_profiles", db_index=True
    )
    provider = models.CharField(
        max_length=20,
        choices=[(p.value, p.name) for p in BrowserProvider],
        db_index=True,
    )
    profile_id = models.CharField(max_length=255)
    folder_id = models.CharField(max_length=255, null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "browser_profile"
        constraints = [
            models.UniqueConstraint(
                fields=["site", "provider"], name="unique_browser_profile"
            ),
            models.CheckConstraint(
                name="browser_provider_valid",
                condition=Q(
                    provider__in=[
                        browser_provider.value for browser_provider in BrowserProvider
                    ]
                ),
            ),
        ]
        indexes = [
            models.Index(fields=["site", "provider"]),
        ]

    def __str__(self):
        return f"{self.provider}_{self.site}"
