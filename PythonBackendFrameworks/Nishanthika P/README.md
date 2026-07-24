# Hands-On 3 — Django REST Views, URL Routing & Forms

## Setup
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py migrate
python manage.py runserver
```

## Auto-generated routes (via DefaultRouter)
```
GET/POST          /api/courses/
GET/PUT/PATCH/DEL /api/courses/{pk}/
GET               /api/courses/{pk}/students/   <- custom @action
GET/POST          /api/students/
GET/PUT/PATCH/DEL /api/students/{pk}/
GET/POST          /api/enrollments/
GET/PUT/PATCH/DEL /api/enrollments/{pk}/
```

## Files
- `coursemanager/courses/serializers.py` — Task 1 ModelSerializers
- `coursemanager/courses/handson3_task1_views_reference.py` — Task 1's original
  APIView-based `CourseListView` / `CourseDetailView` (kept for reference;
  superseded by the ViewSet below)
- `coursemanager/courses/views.py` — Task 2's final `CourseViewSet`,
  `StudentViewSet`, `EnrollmentViewSet` + custom `/students/` action
- `coursemanager/courses/urls.py` — DRF `DefaultRouter` wiring

## Expected Outcome
All 5 HTTP methods work with correct status codes (200/201/204/400/404).
`GET /api/courses/{id}/students/` returns only students enrolled in that course.
