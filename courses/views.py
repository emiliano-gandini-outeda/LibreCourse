from django.http import HttpResponse, JsonResponse
from courses.models import Course, Lesson
import json
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

# Create your views here.
    
def listCourses(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses" : courses})

def courseById(request, id):
    course = get_object_or_404(Course, id = id)
    lessons = course.lesson_set.all().order_by("position")
    return render(request, "course.html", {"course" : course, "lessons" : lessons})

def createCourse(request):
    if request.method != "POST":
        raise(ValueError("Request not valid")) 
    else:
        data = json.loads(request.body)
        course = Course.objects.create(
            title = data.get("title"),
            summary = data.get("summary", ""),
            price = data.get("price", 0),
            tags = data.get("tags"),
            status = "draft"
        )
        return HttpResponse(f"Created course: {course.title}")
    
def updateCourse(request, course_id):
    if request.method != "POST":
        raise(ValueError("Request not valid")) 
    else:
        course = get_object_or_404(Course, id = course_id)
        data = json.loads(request.body)
        course.title = data.get("title", course.title)
        course.summary = data.get("summary", course.summary)
        course.tags = data.get("tags", course.tags)
        course.status = data.get("status", course.status)
        course.save()
        return HttpResponse(f"Updated course: {course.title}")

def publishedCourses(request):
    q = request.GET.get("q", "")
    courses = Course.objects.filter(status="pub")
    if q:
        courses = courses.filter(title__icontains=q)
    return render(request, "courses.html", {"courses": courses})

def createLesson(request, course_id):
    if request.method != "POST":
            raise(ValueError("Request not valid")) 
    else:
        associatedCourse = get_object_or_404(Course, id =  course_id)
        data = json.loads(request.body)
        lesson = Lesson.objects.create(
            title = data.get("title"),
            content = data.get("content"),
            course = associatedCourse,
            duration_minutes = data.get("duration_minutes", 0),
        )
        return HttpResponse(f"Lesson Created: {lesson.title}")

def updateLesson(request, lesson_id):
    if request.method != "POST":
        raise(ValueError("Request not valid"))
    else:
        lesson = get_object_or_404(Lesson, id = lesson_id)
        data = json.loads(request.body)
        lesson.title = data.get("title", lesson.title)
        lesson.content = data.get("content", lesson.content)
        lesson.duration_minutes = data.get("duration_minutes", lesson.duration_minutes)
        lesson.save()
        return HttpResponse(f"Lesson Updated: {lesson.title}")

def deleteLesson(request, lesson_id):
    if request.method != "POST":
        raise(ValueError("Invalid Request"))
    else:
        lesson = get_object_or_404(Lesson, id = lesson_id)
        title = lesson.title
        lesson.delete()
        return HttpResponse(f"Lesson Deleted: {title}")   
    
def deleteCourse(request, course_id):
    if request.method != "POST":
        raise(ValueError("Invalid Request"))
    else:
        course = get_object_or_404(Course, id = course_id)
        lesson_count = course.lesson_set.count()
        title = course.title
        course.delete()
        return HttpResponse(f"Deleted course {title} and {lesson_count} lessons")
    
def reorderLessons(request, course_id):
    if request.method != "POST":
        raise(ValueError("Invalid Request"))
    else:
        course = get_object_or_404(Course, id = course_id)
        data  = json.loads(request.body)
        valid_ids = set(course.lesson_set.values_list("id", flat=True))
        recieved_ids = set(data.get("order",[]))
        if not recieved_ids:
            raise(ValueError("ID Order Requiered"))
        elif valid_ids != recieved_ids:
            raise(ValueError("Invalid Lesson IDs"))
        else:
            recieved_ids = data.get("order", [])
            for positionCounter, lesson_ID in enumerate(recieved_ids, start=1):
                lesson = get_object_or_404(Lesson, id = lesson_ID, course =  course)
                lesson.position = positionCounter
                lesson.save()
            return HttpResponse(f"Order updated: {recieved_ids}")

def toggleCourseStatus(request, course_id):
    if request.method != "POST":
        raise(ValueError("Invalid Request"))
    else:
        course = get_object_or_404(Course, id=course_id)

        if course.status == "draft":
            course.status = "pub"
        else:
            course.status = "draft"

        course.save()
        return HttpResponse(f'Course "{course.title}" status set to {course.status}')

def lessonDetails(request, lesson_id):
    if request.method != "GET":
        raise(ValueError("Invalid Request"))
    else:
        lesson = get_object_or_404(Lesson, id = lesson_id)
        data = {
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "duration_minutes": lesson.duration_minutes,
            "course": {
                "id": lesson.course.id,
                "title": lesson.course.title,
            },
        }
        return JsonResponse(data)
    
def courseDetails(request, course_id):
    if request.method != "GET":
        raise(ValueError("Invalid Request"))
    else:
        course = get_object_or_404(Course, id = course_id)
        lessons = []
        for lesson in course.lesson_set.all().order_by("position"):
            lessons.append({
                "id": lesson.id,
                "title": lesson.title,
                "position": lesson.position,
            })
        data = {
            "id" : course.id,
            "title" : course.title,
            "created_at" : course.created_at,
            "status" : course.status,
            "price" : course.price,
            "tags" : course.tags,
            "lessons" : lessons
        }
        return JsonResponse(data)