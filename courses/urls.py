from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course-home'),
    path('<int:id>/', views.course_page, name = "course-detail")
]