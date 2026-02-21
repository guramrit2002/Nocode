import time
import uuid
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from accounts.models import RequestLog


User = get_user_model()


class RequestLogMiddleware(MiddlewareMixin):
    """
    Synchronous request logging middleware.
    Safe for authentication-heavy no-code platforms.
    """

    def process_request(self, request):
        request._start_time = time.time()
        request._request_id = uuid.uuid4()

    def process_response(self, request, response):
        try:
            if "auth" not in request.path :
                return response
            
            print("[RequestLogMiddleware] Logging request:", request.method, request.path)
            duration_ms = None
            if hasattr(request, "_start_time"):
                duration_ms = int((time.time() - request._start_time) * 1000)

            user = getattr(request, "user", None)

            request_obj = RequestLog.objects.create(
                request_id=getattr(request, "_request_id", None),
                user=user if user and user.is_authenticated else None,
                email=getattr(user, "email", None) if user and user.is_authenticated else None,
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                source="web",
                request_type=self.get_request_type(request),
                duration_ms=duration_ms,
            )
            print(request_obj)
        except Exception:
            # Never block user request due to logging failure
            pass

        return response

    def process_exception(self, request, exception):
        try:
            RequestLog.objects.create(
                request_id=getattr(request, "_request_id", None),
                method=request.method,
                path=request.path,
                status_code=500,
                error_message=str(exception),
                ip_address=self.get_client_ip(request),
                source="web",
                request_type=self.get_request_type(request),
            )
        except Exception:
            pass

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def get_request_type(self, request):
        if request.path.startswith("/auth/"):
            return "auth"
        if request.path.startswith("/admin/"):
            return "admin"
        return "data"
