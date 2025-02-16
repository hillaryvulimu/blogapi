from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from rest_framework import generics, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .serializers import CategorySerializer, PostSerializer, LikeDislikeSerializer

from .models import Post, LikeDislike


# Posts categories
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # List of all categories
        categories = [
            "Strategy", "Party", "Cooperative", "Deck-Building", "Abstract", "Family",
            "Word", "Dice", "Card", "Tile-Laying",
            "Trivia", "Children's", "Role-Playing", "Thematic", "Other"
        ]
        
        # Convert the queryset to a list of dictionaries
        return [{'category': category} for category in categories]


class CategoryDetailAPIView(generics.ListAPIView):
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


# post total reactions
class PostReactionsAPIView(APIView):
    # add cache control so that the front-end always gets up-to-date reactions, not cached ones
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        reactions = LikeDislike.objects.filter(post=post)
        serializer = LikeDislikeSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# current user reaction

class UserReactionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeDislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post_slug = self.kwargs['slug']
        user = self.request.user
                                         
        try:
            post = get_object_or_404(Post, slug=post_slug)
            reaction = LikeDislike.objects.filter(post=post, user=user).first()
  
            return reaction
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except LikeDislike.DoesNotExist:
            return Response({"error": "Reaction not found."}, status=status.HTTP_200_OK)



# Create new reaction
class CreateUserReactionAPIView(generics.CreateAPIView):
    serializer_class = LikeDislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_slug = self.kwargs['slug']
        user = self.request.user

        post = get_object_or_404(Post, slug=post_slug)
        if LikeDislike.objects.filter(post=post, user=user).exists():
            return Response({'detail': 'Reaction already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['post'] = post.id
        data['user'] = user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)