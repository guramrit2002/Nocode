from django.urls import path
from .views import *

urlpatterns = [
    path('send-request/', MagicLinkViewSet.as_view({'post': 'request'}),
         name='magic-link'),
    path('verify/', MagicLinkViewSet.as_view({'post': 'verify'}),
         name='magic-link-verify'),
]