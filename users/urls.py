from django.urls import path
from . import views

urlpatterns = [
    path("", views.listUsers, name = "users"),
    path("login/", views.login_view, name = "login"),
    path("signup/", views.signup_view, name = "signup"),
    path("logout/", views.logout_view, name = "logout"),
    path("user/<int:id>/", views.userDetails, name="user-details"),
]