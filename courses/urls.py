from django.urls import path
from . import views

urlpatterns = [
    path("", views.publishedCourses, name = "courses"),
    path("<int:course_id>/", views.courseById, name = "course_details"),
    path("create/", views.createCourse, name = "create_course"),
    path("<int:course_id>/update/", views.updateCourse, name = "update_course"),
    path("<int:course_id>/delete/", views.deleteCourse, name = "delete_course"),
]