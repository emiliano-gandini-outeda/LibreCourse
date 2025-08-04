from django.urls import path
from .views import RegisterView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="login"),
    path("user/<int:id>/", views.user_details, name="user-details"),
]