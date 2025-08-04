from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=450)
    createdDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"#{self.id} : {self.title}"