from django.db import models

class Department(models.Model):
    dept_name    = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100, blank=True, null=True)
    budget       = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    class Meta:
        db_table = "departments"

class Student(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(max_length=100, unique=True)
    date_of_birth   = models.DateField(null=True, blank=True)
    department      = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    enrollment_year = models.IntegerField(null=True)
    is_active       = models.BooleanField(default=True)
    class Meta:
        db_table = "students"

class Course(models.Model):
    course_name   = models.CharField(max_length=150)
    course_code   = models.CharField(max_length=20, unique=True)
    credits       = models.IntegerField(null=True)
    max_seats     = models.IntegerField(default=60)
    department    = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "courses"

class Enrollment(models.Model):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE)
    course          = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(null=True)
    grade           = models.CharField(max_length=2, null=True, blank=True)
    class Meta:
        db_table = "enrollments"
        unique_together = ("student", "course")

class Professor(models.Model):
    prof_name  = models.CharField(max_length=100)
    email      = models.EmailField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    salary     = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = "professors"

class CourseSchedule(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    class Meta:
        db_table = "course_schedules"
