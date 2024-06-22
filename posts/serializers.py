
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post, Comment, LikeDislike

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = get_user_model()
        fields = ("id", "username", 'first_name', 'last_name') # Also be send to front-end


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer()  # Serialize the User model fields for the commenter
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'commenter', 'text', 'created_at')


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'
        

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Serialize the User model fields for the author
    comments = CommentSerializer(many=True, read_only=True)  # Serialize comments related to the post
    likes_dislikes = LikeDislikeSerializer(many=True, read_only=True)  # Serialize likes/dislikes related to the post
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__' # ( "id", "author", "title", "body", "created_at", "post_pic", )


    # calculate total likes/dislikes
    def get_total_likes(self, obj):
        return obj.likes_dislikes.filter(reaction=LikeDislike.Reaction.LIKE).count()
    
    def get_total_dislikes(self, obj):
        return obj.likes_dislikes.filter(reaction=LikeDislike.Reaction.DISLIKE).count()
    
    
class CategorySerializer(serializers.Serializer):
    category = serializers.CharField()