from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def user_list(request):
    users = User.objects.all()
    return render(request, "users/users.html", {"users" : users})

def user_details(request, id):
    user = get_object_or_404(User, id = id)
    return render(request, "users/user_details.html", {"user" : user})
