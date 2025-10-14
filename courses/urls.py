from django.urls import path
from . import views

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("create/", views.CourseCreateView.as_view(), name="course-create"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
    path(
        "<int:course_id>/lessons/create/",
        views.LessonCreateView.as_view(),
        name="lesson-create",
    ),
    path(
        "<int:course_id>/lessons/<int:lesson_id>/update/",
        views.LessonUpdateView.as_view(),
        name="lesson-update",
    ),
    path(
        "<int:course_id>/lessons/<int:lesson_id>/delete/",
        views.LessonDeleteView.as_view(),
        name="lesson-delete",
    ),
    path(
        "<int:pk>/collaborators/manage/",
        views.ManageCollaboratorsView.as_view(),
        name="course-manage-collaborators",
    ),
    path(
        "collaborators/autocomplete/", views.user_autocomplete, name="user-autocomplete"
    ),
]
