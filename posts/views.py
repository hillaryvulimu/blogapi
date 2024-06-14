from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .serializers import CategorySerializer

from .models import Post


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Query all distinct categories from the Post model
        categories = Post.objects.values_list('category', flat=True).distinct()
        
        # Convert the queryset to a list of dictionaries
        return [{'category': category} for category in categories]