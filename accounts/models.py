from django.contrib.auth.models import AbstractUser
from django.db import models
import os

def user_uploads_path(instance, filename):
    '''
    Determines the file path for uploaded profile pictures.

    Parameters:
    filename (str): the original filename
    
    Returns:
    str: the new file path based on the username and maintaining the extension
    '''
    ext = os.path.splitext(filename)[1]
    new_filename = f'{instance.username}_profile_pic{ext}'
    return f'{instance.username}/profile_pic/{new_filename}' 


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)    
    profile_pic = models.ImageField(upload_to=user_uploads_path, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle profile picture updates.
            
        Deletes the old profile picture if it exists before saving the new one.

        Uploads file to MEDIA_ROOT/<username>/profile_pic/<username>_profile_pic.<ext>
        """
        try:
            # Get the existing profile picture
            existing = CustomUser.objects.get(id=self.id)
            # If the profile picture is being changed and there's an existing one, delete the old file
            if existing.profile_pic and self.profile_pic != existing.profile_pic:
                if os.path.isfile(existing.profile_pic.path):
                    os.unlink(existing.profile_pic.path)

        except CustomUser.DoesNotExist:
            # When the user is being created for the first time, there's no existing profile picture
            pass

        # Save the new profile picture
        super().save(*args, **kwargs)
