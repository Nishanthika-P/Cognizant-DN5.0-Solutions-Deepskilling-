"""
courses/urls.py
Hands-On 1, Task 2, step 9: maps /api/hello/ to hello_view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
]
