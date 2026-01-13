from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'dashboard-user-projects', UserProjectDashboardViewSet,
                basename='dashboard')

urlpatterns = router.urls
