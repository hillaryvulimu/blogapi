from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .viewsets import PostViewSet, UserViewSet

from .views import CategoryListAPIView, CategoryDetailAPIView, PostSearchAPIView, \
    PostReactionsAPIView, UserReactionAPIView, CreateUserReactionAPIView

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("", PostViewSet, basename="posts")

urlpatterns = [
    path('<slug:slug>/reactions/', PostReactionsAPIView.as_view(), name='post-total-reactions'),
    path('<slug:slug>/reactions/user/', UserReactionAPIView.as_view(), name='user-reaction'),
    path('<slug:slug>/reactions/user/create/', CreateUserReactionAPIView.as_view(), name='create-user-reaction'),
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('categories/<str:category>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('search/', PostSearchAPIView.as_view(), name='search'),
    path('', include(router.urls)),
]