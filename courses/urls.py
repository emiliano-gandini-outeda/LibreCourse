from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_home, name='course-home'),
]