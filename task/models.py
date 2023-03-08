from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=200, unique=True)
    avatar = models.FileField(upload_to='uploads/avatars/')
    themes = (
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
    )
    theme = models.CharField(max_length=255, choices=themes)
