"""
courses/urls.py
Hands-On 3, Task 2: DefaultRouter auto-generates all CRUD URL patterns.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('students', views.StudentViewSet)
router.register('enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
    path('', include(router.urls)),
]
