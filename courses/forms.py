from django import forms
from .models import Course, Lesson, Tag
from users.models import User

class CourseForm(forms.ModelForm):
    tags_input = forms.CharField(
    required=False,
    help_text="Enter tags separated by commas. Available tags will appear as suggestions."
)


    class Meta:
        model = Course
        fields = ["title", "description", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Prepopulate tags_input with existing tags
            self.fields["tags_input"].initial = ", ".join(tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # Update tags
        tags_list = [t.strip() for t in self.cleaned_data["tags_input"].split(",") if t.strip()]
        instance.tags.set([Tag.objects.get_or_create(name=t)[0] for t in tags_list])
        return instance


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content"]  # duration_minutes if you want
        labels = {
            "title": "Lesson Title",
            "content": "Lesson Content",
    
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