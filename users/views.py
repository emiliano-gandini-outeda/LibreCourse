from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import SignupForm, LoginForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user with cleaned data
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(
                email=email, 
                username=username, 
                password=password
            )
            
            login(request, user)
            
            return JsonResponse({
                "success": True,
                "message": f"User {user.username} created successfully!"
            })
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    
    return JsonResponse({
        "error": "Invalid request method. Use POST."
    }, status=400)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "success": True,
                    "message": f"Welcome back, {user.username}!"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": {"__all__": ["Invalid email or password"]}
                }, status=401)
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    
    return JsonResponse({
        "error": "Invalid request method. Use POST."
    }, status=400)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({
            "success": True,
            "message": "You have been logged out successfully."
        })
    
    return JsonResponse({
        "error": "Invalid request method. Use POST."
    }, status=400)

def listUsers(request):
    users = User.objects.all()
    return render(request, "users.html", {"users" : users})

def userDetails(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return render(request, "user-details.html", {"user" : user})