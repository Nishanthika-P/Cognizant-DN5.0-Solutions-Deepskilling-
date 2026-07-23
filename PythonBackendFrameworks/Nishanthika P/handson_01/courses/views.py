"""
courses/views.py
Hands-On 1, Task 2, step 8: simple function-based view.
"""
from django.http import HttpResponse


def hello_view(request):
    return HttpResponse('Course Management API is running')
