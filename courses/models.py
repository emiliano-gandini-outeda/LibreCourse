from django.db import models
from users.models import CustomUser


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=450)
    createdDate = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_courses")
    status = models.CharField(max_length=15, choices=[("pub", "Public"), ("priv", "Private"), ("dra", "Draft")])
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    favorites = models.ManyToManyField(CustomUser, blank=True, related_name="favorite_courses")
    collaborators = models.ManyToManyField(CustomUser, blank=True, related_name="collaborating_courses")
    def __str__(self):
        return f"{self.title} #{self.id}"
    
class Lesson(models.Model):
    title = models.CharField(max_length=30)