from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings
from .models import Course
from django.http import HttpResponse

# Create your views here.

def course_home(request):
        return render(request, 'courses/home.html')
    
def course_page(request, id):
        tzname = request.COOKIES.get("user_timezone")
        
        if tzname:
            timezone.activate(tzname)
        
        course = get_object_or_404(Course, id = id)
        return render(request, "courses/course_detail.html", {"course" : course})
    
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/home.html", {"courses" : courses})