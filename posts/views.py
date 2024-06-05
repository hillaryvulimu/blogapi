
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .permissions import IsAuthorOrReadOnly

from .models import Post

from .serializers import PostSerializer

def common_fields():
    return {
        'queryset': Post.objects.all(),
        'serializer': PostSerializer,
        'permission_classes': (IsAuthorOrReadOnly,),
    }

class PostList(ListCreateAPIView):
    queryset = common_fields()['queryset']
    serializer_class = common_fields()['serializer']
    permission_classes = common_fields()['permission_classes']


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = common_fields()['queryset']
    serializer_class = common_fields()['serializer']
    permission_classes = common_fields()['permission_classes']


