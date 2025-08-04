from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User


# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

def user_list(request):
    users = User.objects.all()
    return render(request, "users/users.html", {"users" : users})

def user_details(request, id):
    user = get_object_or_404(User, id = id)
    return render(request, "users/user_details.html", {"user" : user})

def form_invalid(self, form):
    print("Form errors:", form.errors)
    return super().form_invalid(form)