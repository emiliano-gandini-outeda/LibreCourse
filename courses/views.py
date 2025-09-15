from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Case, When, Value, IntegerField, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from courses.forms import CourseForm, LessonForm, CollaboratorsForm
from courses.models import Course, Lesson, Tag, PendingCollaborator
from users.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.signing import Signer



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass a plain list of tag names
        context["all_tags"] = list(Tag.objects.values_list("name", flat=True))
        return context

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
    
    def get_object(self, queryset=None):
        lesson_id = self.kwargs.get("lesson_id")
        return get_object_or_404(Lesson, id=lesson_id)

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
    login_url = reverse_lazy("login")

    def test_func(self):
        # Only the creator can manage collaborators
        return self.request.user == self.get_object().creator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # All pending collaborators
        pending = course.pending_collaborators.all()
        # Show display_name if user exists, else email
        pending_info = []
        for p in pending:
            user = User.objects.filter(email__iexact=p.email).first()
            pending_info.append({
                "display_name": user.display_name if user else None,
                "email": p.email,
                "exists": bool(user),
                "profile_picture": user.profile_picture if user else None
            })

        context["pending_collaborators"] = pending_info
        context["all_users"] = User.objects.exclude(pk=course.creator.pk)
        return context

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        signer = Signer()

        # Handle removing confirmed collaborator
        remove_user_id = request.POST.get("remove_user_id")
        if remove_user_id:
            user = get_object_or_404(User, id=remove_user_id)
            course.collaborators.remove(user)
            return redirect("course-manage-collaborators", pk=course.pk)

        # Handle removing pending collaborator
        remove_pending_email = request.POST.get("remove_pending_email")
        if remove_pending_email:
            pending = course.pending_collaborators.filter(email=remove_pending_email).first()
            if pending:
                pending.delete()
            return redirect("course-manage-collaborators", pk=course.pk)

        # Handle adding multiple users by username/ID
        new_users = request.POST.getlist("new_users[]")  # array of usernames or IDs
        for identifier in new_users:
            identifier = identifier.strip()
            if not identifier:
                continue

            # Lookup user by ID or username
            user = None
            if identifier.isdigit():
                user = User.objects.filter(pk=int(identifier)).first()
            if not user:
                user = User.objects.filter(username__iexact=identifier).first()
            
            if user and user != course.creator:
                # Stage as pending
                pending, created = PendingCollaborator.objects.get_or_create(course=course, email=user.email)
                token = signer.sign(f"{course.pk}:{user.email}")
                accept_url = request.build_absolute_uri(reverse("accept-collaborator-invite", kwargs={"token": token}))
                send_mail(
                    subject=f"You've been invited to collaborate on {course.title}",
                    message=f"Hi {user.username},\n\n{request.user.display_name} invited you to collaborate on {course.title}.\nClick to accept: {accept_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

        # Handle adding multiple emails
        new_emails = request.POST.getlist("new_emails[]")  # array of emails
        for email in new_emails:
            email = email.strip()
            if not email:
                continue
            pending, created = PendingCollaborator.objects.get_or_create(course=course, email=email)
            token = signer.sign(f"{course.pk}:{email}")
            accept_url = request.build_absolute_uri(reverse("accept-collaborator-invite", kwargs={"token": token}))
            send_mail(
                subject=f"You've been invited to collaborate on {course.title}",
                message=f"Hi,\n\n{request.user.display_name} invited you to collaborate on {course.title}.\nClick to accept: {accept_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

        return redirect("course-manage-collaborators", pk=course.pk)

    def get_success_url(self):
        return reverse("course-manage-collaborators", kwargs={"pk": self.object.pk})

# JSON endpoint for autocomplete

@require_GET
def user_autocomplete(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        qs = User.objects.filter(
            Q(username__icontains=query) | Q(id__iexact=query)
        ).exclude(pk=request.user.pk)[:10]

        results = [
            {
                "id": u.id,
                "display_name": u.display_name,
                "username": u.username,
                "profile_picture": u.profile_picture or "/static/default_avatar.png"
            }
            for u in qs
        ]
    return JsonResponse(results, safe=False)
