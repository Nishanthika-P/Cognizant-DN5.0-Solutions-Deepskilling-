"""
coursemanager URL Configuration
One-line role: Root URL configuration - maps incoming URL paths to
views (directly or via include() to app-level urls.py files).
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),  # delegate /api/* to the courses app
]
