
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from rest_framework.permissions import IsAdminUser

from .permissions import IsAuthorOrReadOnly

from .models import Post

from .serializers import PostSerializer, UserSerializer

# Using viewsets
# check commit 2e2693993ddaf339900b4d3be63b41bd42423cd2 for PostList/PostDetail before vieset
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = IsAdminUser, # only admins can see a list of authors
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer