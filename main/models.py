from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# User = get_user_model()


class Post(models.Model):
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)
