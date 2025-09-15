from courses.models import Course, Lesson, Tag
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Case, When, Value, IntegerField, Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from courses.forms import CourseForm, LessonForm, CollaboratorsForm
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404

# Create your views here.
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.filter(status="pub").distinct()
        q = self.request.GET.get("q", "").strip()
        tag_filter = self.request.GET.get("tag", "").strip()

        if q:
            # Search priority: title=1, tag=2, description=3
            queryset = queryset.annotate(
                priority=Case(
                    When(title__icontains=q, then=Value(1)),
                    When(tags__name__icontains=q, then=Value(2)),
                    When(description__icontains=q, then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField()
                )
            ).filter(
                Q(title__icontains=q) |
                Q(tags__name__icontains=q) |
                Q(description__icontains=q)
            ).order_by('priority', 'title')

        if tag_filter:
            queryset = queryset.filter(tags__name__iexact=tag_filter)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_tags"] = Tag.objects.all()
        context["current_q"] = self.request.GET.get("q", "")
        context["current_tag"] = self.request.GET.get("tag", "")
        return context

class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object

        # Lessons ordered by position
        context["lessons"] = course.lesson_set.all().order_by("position")

        # Related courses: share at least one tag or same creator, exclude self
        context["related_courses"] = Course.objects.filter(
            status="pub"
        ).filter(
            Q(tags__in=course.tags.all()) | Q(creator=course.creator)
        ).exclude(id=course.id).distinct()[:5]

        return context
    
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"  # Django default would be courses/course_form.html anyway

    def form_valid(self, form):
        # assign creator before saving
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})



class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().creator

    def get_success_url(self):
        return reverse("course-list")
    
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"  # same as create view, can reuse

    def test_func(self):
        # Only the creator can edit the course
        return self.request.user == self.get_object().creator

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})

class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "courses/lesson_form.html"

    def test_func(self):
        course_id = self.kwargs["course_id"]
        course = get_object_or_404(Course, id=course_id)
        return self.request.user == course.creator or self.request.user in course.collaborators.all()

    def form_valid(self, form):
        course_id = self.kwargs["course_id"]
        form.instance.course = get_object_or_404(Course, id=course_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.course.pk})

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs["course_id"]
        course = get_object_or_404(Course, id=course_id)
        initial["position"] = course.lesson_set.count() + 1
        return initial

class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "courses/lesson_form.html"

    def test_func(self):
        lesson = self.get_object()
        course = lesson.course
        return self.request.user == course.creator or self.request.user in course.collaborators.all()

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.course.pk})

class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = "courses/lesson_confirm_delete.html"

    def test_func(self):
        lesson = self.get_object()
        course = lesson.course
        return self.request.user == course.creator  # collaborators cannot delete

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.course.pk})


class ManageCollaboratorsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CollaboratorsForm
    template_name = "courses/manage_collaborators.html"

    def test_func(self):
        # Only creator can manage collaborators
        return self.request.user == self.get_object().creator

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})

