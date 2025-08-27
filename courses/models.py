from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Max

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=450)
    createdDate = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name=(_("created_courses")))
    status = models.CharField(max_length=15, choices=[("pub", "Public"), ("priv", "Private"), ("dra", "Draft")])
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    favorites = models.ManyToManyField(CustomUser, blank=True, related_name="favorite_courses")
    collaborators = models.ManyToManyField(CustomUser, blank=True, related_name="collaborating_courses")
    def __str__(self):
        return f"{self.title} #{self.id}"
    
class Lesson(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(_("lesson_contents"))
    course = models.ForeignKey(Course, verbose_name=_("lessons"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField()
    class Meta:
        ordering = ["order"]

@receiver([post_save, post_delete], sender=Lesson)
def update_course_timestamp(sender, instance, **kwargs):
    course = instance.course
    course.save()