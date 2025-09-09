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
            return redirect('home') 
        
        # If form is invalid, fall through to render form with errors
    
    else:  # GET request
        form = SignupForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:

                form.add_error(None, "Invalid email or password")
        # If form is invalid, fall through to render with errors
    
    else:  # GET request
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == "POST" or request.method == "GET":
        logout(request)
        return redirect('home')
    
    return JsonResponse({
        "error": "Invalid request method. Use POST."
    }, status=400)

def listUsers(request):
    users = User.objects.all().order_by('id')
    return render(request, "users/users.html", {"users" : users})

def userDetails(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return render(request, "users/user-details.html", {"user" : user})

def userProfile(request):
    return render(request, "users/profile.html")