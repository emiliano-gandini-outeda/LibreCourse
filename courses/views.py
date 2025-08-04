from django.shortcuts import render, get_object_or_404

from django.conf import settings
from .models import Course
# Create your views here.
from django.http import HttpResponse

print("TEMPLATE DIRS:", settings.TEMPLATES[0]['DIRS'])

def course_home(request):
        return render(request, 'courses/home.html')
    
def course_page(request, id):
        course = get_object_or_404(Course, id = id)
        return render(request, "courses/course_detail.html", {"course" : course})