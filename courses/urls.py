from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_home, name='course-home'),
    path('<int:id>/', views.course_page, name = "course-detail")
]