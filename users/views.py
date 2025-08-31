from django.http import HttpResponse, JsonResponse
from users.models import User
import json
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def password_valid(password):
    special_chars = "!@#$%^&*()-_+="

    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isdigit() for c in password):
        return False, "Password must include a number"
    if not any(c.isalpha() for c in password):
        return False, "Password must include a letter"
    if not any(c in special_chars for c in password):
        return False, "Password must include a special character"

    return True, ""


def signup_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    email = request.POST.get("email")
    password = request.POST.get("password").strip()

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"})

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Email is not valid"})
    
    is_valid, msg = password_valid(password)
    
    if not is_valid:
        return JsonResponse({"error": msg})
    
    else:
        username = request.POST.get("username")
        user = User.objects.create_user(email=email, username=username, password=password)
        return JsonResponse({"success": f"User {user.username} created!"})

def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status = 400)
    
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request, email = email, password = password)

    if user is None:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    login(request, user)
    return JsonResponse({"message": f"Welcome, {user.username}!"})



def logout_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    logout(request)
    return JsonResponse({"message": "You have been logged out successfully."})

def listUsers(request):
    users = User.objects.all()
    return render(request, "users.html", {"users" : users})

def userDetails(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return render(request, "user-details.html", {"user" : user})