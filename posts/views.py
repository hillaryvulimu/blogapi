
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Post

from .serializers import PostSerializer

def common_fields():
    return {
        'queryset': Post.objects.all(),
        'serializer': PostSerializer
    }

class PostList(ListCreateAPIView):
    queryset = common_fields()['queryset']
    serializer_class = common_fields()['serializer']

class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = common_fields()['queryset']
    serializer_class = common_fields()['serializer']


