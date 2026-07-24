# Hands-On 2 — Django Models, ORM & Admin Interface

## Setup
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell   # confirm tables exist, then .quit / .exit
```

## Task 2: run the ORM queries script. 
```bash
python manage.py shell < ../orm_queries.py
```

## Task 3: admin
```bash
python manage.py createsuperuser   # admin / admin@college.edu / Admin@123
python manage.py runserver
# visit http://127.0.0.1:8000/admin/
```

## Files
- `coursemanager/courses/models.py` — Department, Course, Student, Enrollment
- `coursemanager/courses/admin.py` — admin registrations with list_display/search_fields/list_filter
- `orm_queries.py` — Task 2 ORM query script (filter, annotate, select_related, F())

## Expected Outcome
`showmigrations` shows all applied. Admin lists courses with name/code/credits/department,
search and department filter work. Re-enrolling the same student in the same course raises
a validation error.
