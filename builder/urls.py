from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'project-publish-save', ProjectPublishSaveViewSet, 
                basename='project-publish-save')

urlpatterns = router.urls
