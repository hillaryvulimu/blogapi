from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import UserProfileViewSet


router = DefaultRouter()
router.register('', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
