"""
handson3_task1_views_reference.py
Hands-On 3, Task 1 (reference / pre-refactor version):
APIView-based CourseListView and CourseDetailView, BEFORE they were
replaced by CourseViewSet in Task 2. Kept here for grading /
comparison purposes - not imported by the running app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import CourseSerializer


class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
