from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def course_home(request):
        return HttpResponse("This is the course homepage.")
    
    