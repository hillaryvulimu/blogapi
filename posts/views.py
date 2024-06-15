
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .serializers import CategorySerializer, PostSerializer

from .models import Post


# Posts categories
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Query all distinct categories from the Post model
        categories = Post.objects.values_list('category', flat=True).distinct()
        
        # Convert the queryset to a list of dictionaries
        return [{'category': category} for category in categories]


class CategoryDetailAPIView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(category=category)


# Search
class PostSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(body__icontains=query) |
                Q(category__icontains=query)
                # | Q(author__first_name__icontains=query)  # Search by author's first name
                # | Q(author__last_name__icontains=query)    # Search by author's last name   
            )
        else:
            posts = Post.objects.all()
            # posts = { 'error': 'No results matching your query.'}
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

