"""
courses/views.py
Hands-On 3:
  Task 1 - APIView-based CourseListView / CourseDetailView (see git history
           / HandsOn3_Task1_views.py for the original APIView version).
  Task 2 - Final version: ViewSets + a custom @action (this is what
           courses/urls.py wires up via the DRF router).
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer


def hello_view(request):
    """Hands-On 1, Task 2 view - kept for continuity."""
    return HttpResponse('Course Management API is running')


class CourseViewSet(viewsets.ModelViewSet):
    """
    Provides list/create/retrieve/update/destroy for Course - all 5 CRUD
    operations via ModelViewSet (Hands-On 3, Task 2, step 31).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """GET /api/courses/{id}/students/ - Task 2, step 34."""
        course = self.get_object()
        enrolled_students = [e.student for e in course.enrollment_set.all()]
        serializer = StudentSerializer(enrolled_students, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
