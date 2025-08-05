from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("user/<int:id>/", views.user_details, name="user-details"),
]