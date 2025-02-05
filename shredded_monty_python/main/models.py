from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Model representing a user profile.

    Extends the built-in User model by adding a profile picture field.
    Each Profile instance is associated with a unique User instance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        default='profile_pictures/default_avatar.jpg'
    )
