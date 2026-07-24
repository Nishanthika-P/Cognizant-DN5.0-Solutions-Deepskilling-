"""
courses/admin.py
Hands-On 2, Task 3: register models with the Django admin.
"""
from django.contrib import admin
from .models import Department, Course, Student, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_of_dept', 'budget']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'department']
    search_fields = ['name', 'code']
    list_filter = ['department']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'grade']
