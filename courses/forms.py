from django import forms
from .models import Course, Lesson
from users.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "status", "tags"]  # creator will be auto-filled in view
        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "status": forms.Select(),
            "tags": forms.SelectMultiple(),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content", "position"]  # duration_minutes if you want
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Lesson title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Lesson content"}),
            "position": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
        labels = {
            "title": "Lesson Title",
            "content": "Lesson Content",
            "position": "Lesson Order",
        }
        help_texts = {
            "position": "Number indicating the order of the lesson in the course.",
        }

class CollaboratorsForm(forms.ModelForm):
    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    class Meta:
        model = Course
        fields = ["collaborators"]