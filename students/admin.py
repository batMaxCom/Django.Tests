from django.contrib import admin

# Register your models here.
from students.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass