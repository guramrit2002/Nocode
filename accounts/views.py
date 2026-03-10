import secrets
import hashlib
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ViewSet
from rest_framework import status as status_code
from rest_framework_simplejwt.tokens import RefreshToken
from backend_nocode.utils import response
from accounts.models import CommunicationLog
from accounts.utils import send_login_link



class MagicLinkViewSet(ViewSet):

    def request(self, request):
        try:
            email = request.data.get("email")
            name = request.data.get("name")
            if not email:
                return response(
                    "Email is required",
                    status=status_code.HTTP_400_BAD_REQUEST
                )

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": name, "is_active": True},
            )

            # 1. Generate raw token
            raw_token = secrets.token_urlsafe(32)

            # 2. Hash token (deterministic)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            
            # 3. Expiry time is set to 15 minutes from now
            expires_at = timezone.now() + timedelta(minutes=15)
            
            # 3. Save communication log
            CommunicationLog.objects.create(
                user=user,
                email=email,
                purpose="SEND_TOKEN",
                challenge_hash=token_hash,
                provider="LOCAL",
                expires_at=expires_at,
            )

            # 4. Send RAW token in URL
            url = f"{settings.FRONTEND_URL}/verify?token={raw_token}"

            # 5. Send email with magic link
            send_login_link(name, email, url)
            
            return response(
                message="login link has been sent.",
                data={"url": url, "expiry_time": expires_at},
                status=status_code.HTTP_200_OK
            )

        except Exception as e:
            return response(
                "Something went wrong",
                {"error": str(e)},
                status=status_code.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def verify(self, request):
        try:
            raw_token = request.data.get("token")
            if not raw_token:
                return response(
                    message="Invalid or expired link",
                    data={"error": "Token is required"},
                    status=status_code.HTTP_400_BAD_REQUEST
                )

            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

            log = CommunicationLog.objects.filter(
                challenge_hash=token_hash,
                status="PENDING",
                expires_at__gt=timezone.now()
            ).first()

            if not log:
                return response(
                    message="This login link has expired. Please request a new one.",
                    data={"error": "Invalid or expired token"},
                    status=status_code.HTTP_400_BAD_REQUEST
                )

            user = log.user

            # Mark token as used
            log.status = "COMPLETED"
            log.completed_at = timezone.now()
            log.save(update_fields=["status", "completed_at"])

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # change user active status to True if it is False (for first time login)
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
                return response(
                    message="User activated and login successful",
                    data={
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    },
                    status=status_code.HTTP_200_OK
                )

            return response(
                "Login successful",
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "expires_in": refresh.access_token.lifetime.total_seconds()
                },
                status=status_code.HTTP_200_OK
            )

        except Exception as e:
            return response(
                "Something went wrong",
                {"error": str(e)},
                status=status_code.HTTP_500_INTERNAL_SERVER_ERROR
            )