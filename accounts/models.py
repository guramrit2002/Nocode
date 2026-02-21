import secrets
import hashlib
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class MagicToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="magic_tokens"
    )

    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True)

    def is_valid(self):
        return self.used_at is None and timezone.now() < self.expires_at

    @classmethod
    def generate_for_user(cls, user, ip=None):
        raw_token = secrets.token_urlsafe(32)
        hash_obj = hashlib.sha256(raw_token.encode())
        
        # Create record
        cls.objects.create(
            user=user,
            token_hash=hash_obj.hexdigest(),
            expires_at=timezone.now() + timedelta(minutes=15),
            ip_address=ip
        )
        return raw_token # Return the raw string to be emailed


class RequestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    request_id = models.UUIDField(default=uuid.uuid4, db_index=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="request_logs"
    )

    email = models.EmailField(null=True, blank=True, db_index=True)

    method = models.CharField(max_length=10)
    path = models.CharField(max_length=512)
    status_code = models.PositiveSmallIntegerField()

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    source = models.CharField(
        max_length=50,
        default="web",
        help_text="web / api / worker"
    )

    request_type = models.CharField(
        max_length=50,
        help_text="auth / data / admin / internal"
    )

    duration_ms = models.PositiveIntegerField(null=True, blank=True)

    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "request_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["email"]),
            models.Index(fields=["request_type"]),
            models.Index(fields=["status_code"]),
        ]

    def __str__(self):
        return f"{self.method} {self.path} [{self.status_code}]"


class CommunicationLog(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("EXPIRED", "Expired"),
        ("FAILED", "Failed"),
    ]

    CHANNEL_CHOICES = [
        ("EMAIL", "Email")
    ]

    PURPOSE_CHOICES = [
        ("SEND_TOKEN", "Send Token"),
        ("VERIFY_EMAIL", "Verify Email"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="communication_logs"
    )
    email = models.EmailField(db_index=True)
    channel = models.CharField(
        max_length=30,
        choices=CHANNEL_CHOICES,
        default="EMAIL"
    )
    purpose = models.CharField(
        max_length=50,
        choices=PURPOSE_CHOICES
    )
    challenge_hash = models.CharField(
        max_length=255,
        help_text="Hashed token only"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    provider = models.CharField(
        max_length=50
    )
    failure_reason = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.email} - {self.purpose} - {self.status}"
