from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.listUsers, name = "users"),
    path("login/", views.login_view, name = "login"),
    path("signup/", views.signup_view, name = "signup"),
    path("logout/", views.logout_view, name = "logout"),
    path("user/<int:id>/", views.userDetails, name="user-details"),
    path("profile/", views.userProfile, name="profile"),
    path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), 
         name="password_reset"),
    path("password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), 
         name="password_reset_complete"),
]

