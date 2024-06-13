import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify

def user_uploads_path(instance, filename):
    '''
    Determines the file path for uploaded post picture.

    Parameters:
    filename (str): the original filename
    
    Returns:
    str: the new file path based on the id and slug, and maintaining the extension
    '''
    ext = os.path.splitext(filename)[1]
    new_filename = f'{instance.slug}{ext}'
    return f'{instance.author.username}/posts_images/{new_filename}' 

class Post(models.Model):
    class Category(models.TextChoices):
        STRATEGY = "Strategy", "Strategy"
        PARTY = "Party", "Party"
        COOPERATIVE = "Cooperative", "Cooperative"
        DECK_BUILDING = "Deck-Building", "Deck-Building"
        ROLE_PLAYING = "Role-Playing", "Role-Playing"
        ABSTRACT = "Abstract", "Abstract"
        FAMILY = "Family", "Family"
        THEMATIC = "Thematic", "Thematic"
        WORD = "Word", "Word"
        DICE = "Dice", "Dice"
        CARD = "Card", "Card"
        MINIATURES = "Miniatures", "Miniatures"
        WARGAME = "Wargame", "Wargame"
        LEGACY = "Legacy", "Legacy"
        TILE_LAYING = "Tile-Laying", "Tile-Laying"
        ECONOMIC = "Economic", "Economic"
        DEDUCTION = "Deduction", "Deduction"
        BLUFFING = "Bluffing", "Bluffing"
        TRIVIA = "Trivia", "Trivia"
        CHILDRENS = "Children's", "Children's"

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_pic = models.ImageField(upload_to=user_uploads_path, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.STRATEGY)
    visits_count = models.IntegerField(default=0)


    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle post picture updates.
            
        Deletes the old picture if it exists before saving the new one.

        Uploads file to MEDIA_ROOT/<author>/posts_images/slug.<ext>

        Create a slug from the post title.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        # Check if the post already exists to avoid trying to get an id of None
        if self.id:
            try:
                # Get the existing post
                existing = Post.objects.get(id=self.id)
                # If the picture is being changed and there's an existing one, delete the old file
                if existing.post_pic and self.post_pic and existing.post_pic != self.post_pic:
                    if os.path.isfile(existing.post_pic.path):
                        os.unlink(existing.post_pic.path)
            except Post.DoesNotExist:
                pass
        
        # Save the new picture
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter} on {self.post.title}"
    

class LikeDislike(models.Model):
    class Reaction(models.TextChoices):
        LIKE = "Like", "Like"
        DISLIKE = "Dislike", "Dislike"
        NEITHER = "Neither", 'None'

    post = models.ForeignKey(Post, related_name='likes_dislikes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=Reaction.choices, default=Reaction.NEITHER)

    class Meta:
        unique_together = [['post', 'user']]  # Ensure each user can only like/dislike a post once

    def __str__(self):
        return f"{self.reaction} by {self.user} on {self.post.title}"
