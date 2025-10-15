from django.contrib import admin
from .models import Course, Lesson, Tag


# -------------------------
# Tag Admin
# -------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -------------------------
# Lesson Inline for Courses
# -------------------------
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # number of empty forms
    fields = ("title", "position", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("position",)


# -------------------------
# Course Admin
# -------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "status", "created_at", "updated_at")
    search_fields = (
                    "title",
                    "description",
                    "creator__email",
                    "creator__username"
                    )
    list_filter = ("status", "tags")
    ordering = ("-created_at",)
    filter_horizontal = ("tags", "favorites", "collaborators")
    inlines = [LessonInline]

    fieldsets = (
        (None, {"fields": ("title", "description", "creator", "status")}),
        ("Relations", {"fields": ("tags", "favorites", "collaborators")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


# -------------------------
# Lesson Admin (Optional standalone)
# -------------------------
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "created_at")
    search_fields = ("title", "content", "course__title")
    list_filter = ("course",)
    ordering = ("course", "position")
    readonly_fields = ("created_at",)
