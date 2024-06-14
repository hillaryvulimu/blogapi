from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .serializers import CategorySerializer, PostSerializer

from .models import Post


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