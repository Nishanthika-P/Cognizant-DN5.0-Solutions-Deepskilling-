"""
orm_queries.py
Hands-On 2, Task 2: Django ORM queries.
Run with:  python manage.py shell < ../orm_queries.py
(from inside the coursemanager/ directory)
"""
from courses.models import Department, Course, Student, Enrollment
from django.db.models import Count, F

# 16. Create sample data
cs = Department.objects.create(name='Computer Science', head_of_dept='Dr. Rao', budget=500000)
ee = Department.objects.create(name='Electronics', head_of_dept='Dr. Iyer', budget=350000)

c1 = Course.objects.create(name='Data Structures', code='CS101', credits=4, department=cs)
c2 = Course.objects.create(name='Operating Systems', code='CS102', credits=4, department=cs)
c3 = Course.objects.create(name='Digital Circuits', code='EE101', credits=3, department=ee)
c4 = Course.objects.create(name='Signals & Systems', code='EE102', credits=3, department=ee)

for i, (fn, ln) in enumerate([
    ('Asha', 'Menon'), ('Ravi', 'Kumar'), ('Neha', 'Shah'),
    ('Vikram', 'Rao'), ('Priya', 'Nair'),
], start=1):
    Student.objects.create(
        first_name=fn, last_name=ln, email=f'{fn.lower()}{i}@college.edu',
        department=cs if i % 2 else ee, enrollment_year=2023,
    )

# 17. Filter courses in a specific department (double-underscore lookup)
cs_courses = Course.objects.filter(department__name='Computer Science')
print('CS courses:', list(cs_courses))

# 18. Annotate: count courses per department
dept_counts = Department.objects.annotate(course_count=Count('courses'))
for d in dept_counts:
    print(d.name, d.course_count)

# 19. select_related to avoid N+1 queries
from django.db import connection, reset_queries
reset_queries()
students = Student.objects.select_related('department').all()
for s in students:
    _ = s.department.name if s.department else None  # no extra query fired
print('Query count with select_related:', len(connection.queries))

# 20. Bulk update using F() - computed in the database, not in Python
Department.objects.update(budget=F('budget') * 1.1)
print('Budgets updated by 10%')
