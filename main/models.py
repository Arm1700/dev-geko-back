from django.db import models

class Category(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class PopularCourse(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    lectures = models.IntegerField()
    quizzes = models.IntegerField()
    duration = models.CharField(max_length=50)
    skill_level = models.CharField(max_length=50)
    lang = models.CharField(max_length=50)
    students = models.IntegerField()
    assessments = models.CharField(max_length=10)
    desc = models.TextField()
    certification = models.TextField()
    outcomed = models.JSONField()  # Stores an array of outcomes

    def __str__(self):
        return self.title
