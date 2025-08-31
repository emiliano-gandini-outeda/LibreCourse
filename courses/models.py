from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import User

def get_deleted_user():
    """Function to get or create a deleted user for on_delete"""
    return User.objects.get_or_create(
        email="deleted@example.com",
        defaults={"username": "Deleted User", "is_active": False}
    )[0]

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=450)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name="courses", null=True, blank=True)    
    status = models.CharField(max_length=15, choices=[("pub", "Public"), ("priv", "Private"), ("dra", "Draft")], default="dra")
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    favorites = models.ManyToManyField(User, blank=True, related_name="favorite_courses")
    collaborators = models.ManyToManyField(User, blank=True, related_name="collaborating_courses")
    def __str__(self):
        return f"{self.title} #{self.id}"
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "study_courses"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "status"],
                name="unique_course_title_status"
            )
        ]
    
class Lesson(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(_("lesson_contents"))
    course = models.ForeignKey(Course, verbose_name=_("lessons"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(_("Lesson Order"))

    class Meta:
        ordering = ["-position"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        db_table = "study_lessons"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "course"],
                name="unique_colessourse_lesson_status"
            )
        ]

@receiver([post_save, post_delete], sender=Lesson)
def update_course_timestamp(sender, instance, **kwargs):
    course = instance.course
    course.save()