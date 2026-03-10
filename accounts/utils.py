import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

def send_login_link(name,email, url):
    context = {
        "user_name": name,
        "magic_url": url
    }
    subject = "Login Request for NoCode"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = email
    html_content = render_to_string("auth/magic_link_email.html", context)
    email_message = EmailMultiAlternatives(subject, html_content, 
                                           from_email, [to_email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
    