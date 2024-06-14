from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .viewsets import PostViewSet, UserViewSet

from .views import CategoryListAPIView, CategoryDetailAPIView

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("", PostViewSet, basename="posts")

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('categories/<str:category>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('', include(router.urls)),
]