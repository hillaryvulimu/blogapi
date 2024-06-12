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
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_pic = models.ImageField(upload_to=user_uploads_path, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    
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
