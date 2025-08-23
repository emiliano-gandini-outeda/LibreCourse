from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("user/<int:id>/", views.user_details, name="user-details"),
]