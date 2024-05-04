from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='category_photos/')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='lesson_photos/')
    course_description = models.TextField()
    certification_info = models.TextField()

    def __str__(self):
        return self.name
