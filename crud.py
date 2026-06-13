"""
HANDS-ON 6 — Tasks 2 & 3: CRUD via SQLAlchemy ORM + N+1 Fix
File: crud.py

QUERY COUNT ANALYSIS (with echo=True):
  Task 2 Step 5 (naive):  Issues 1 query per enrollment to load student/course
                          → ~11 SQL statements for 10 enrollments (N+1 problem)
  Task 3 (joinedload):    Issues 1 SQL statement with JOINs — all data in one go
  Improvement:            13 queries → 1 query (13x fewer round-trips)
"""

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Department, Student, Course, Enrollment, Professor

# ── Engine & Session ──────────────────────────────────────────────────────────
DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/college_db_orm"
engine  = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL in console
Session = sessionmaker(bind=engine)


# ── Task 2: CRUD Operations ───────────────────────────────────────────────────

def task2_insert_data():
    session = Session()
    try:
        # 81: Add 3 Departments
        depts = [
            Department(dept_name="Computer Science", head_of_dept="Dr. Ramesh Kumar", budget=850000.00),
            Department(dept_name="Computer and communication",      head_of_dept="Dr. Priya Nair",   budget=620000.00),
            Department(dept_name="Mechanical",       head_of_dept="Dr. Suresh Iyer",  budget=540000.00),
        ]
        session.add_all(depts)
        session.commit()
        print("Departments inserted")

        #  81: Add 5 Students
        students = [
            Student(first_name="Arjun",  last_name="Mehta",  email="arjun.mehta@college.edu",
                    date_of_birth=date(2003,4,12),  department_id=1, enrollment_year=2022),
            Student(first_name="Priya",  last_name="Suresh", email="priya.suresh@college.edu",
                    date_of_birth=date(2003,7,25),  department_id=1, enrollment_year=2022),
            Student(first_name="Nisha",  last_name="Verma",  email="nisha.verma@college.edu",
                    date_of_birth=date(2002,11,8),  department_id=2, enrollment_year=2021),
            Student(first_name="Sneha",  last_name="Patel",  email="sneha.patel@college.edu",
                    date_of_birth=date(2004,1,30),  department_id=3, enrollment_year=2023),
            Student(first_name="Vikram", last_name="Das",    email="vikram.das@college.edu",
                    date_of_birth=date(2003,9,14),  department_id=1, enrollment_year=2022),
        ]
        session.add_all(students)
        session.commit()
        print("Students inserted")

        # 82: Add 3 Courses
        courses = [
            Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=1),
            Course(course_name="Database Management Systems",  course_code="CS102", credits=3, department_id=1),
            Course(course_name="Circuit Theory",               course_code="EC101", credits=3, department_id=2),
        ]
        session.add_all(courses)
        session.commit()
        print("Courses inserted")

        # 82: Add 4 Enrollments
        enrollments = [
            Enrollment(student_id=1, course_id=1, enrollment_date=date(2022,7,1), grade='A'),
            Enrollment(student_id=1, course_id=2, enrollment_date=date(2022,7,1), grade='B'),
            Enrollment(student_id=2, course_id=1, enrollment_date=date(2022,7,1), grade='B'),
            Enrollment(student_id=3, course_id=3, enrollment_date=date(2021,7,1), grade='A'),
        ]
        session.add_all(enrollments)
        session.commit()
        print(" Enrollments inserted")

    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()


def task2_read_cs_students():
    """ 83: Query students in Computer Science department"""
    session = Session()
    students = (
        session.query(Student)
        .join(Department)
        .filter(Department.dept_name == "Computer Science")
        .all()
    )
    print("\n── CS Students ──────────────────────────────────")
    for s in students:
        print(f"  {s.first_name} {s.last_name} ({s.email})")
    session.close()
    return students


def task2_read_enrollments_naive():
    """
    84 (NAIVE): N+1 problem — triggers extra queries for each enrollment
    """
    session = Session()
    print("\n── Enrollments (NAIVE — N+1) ────────────────────")
    enrollments = session.query(Enrollment).all()  # 1 query
    for e in enrollments:
        # Each access to e.student and e.course fires a separate SELECT (lazy load)
        print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | Grade: {e.grade}")
    session.close()


def task2_update_student():
    """ 85: Update a student's enrollment_year by email"""
    session = Session()
    student = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
    if student:
        student.enrollment_year = 2023
        session.commit()
        print(f"\n Updated {student.first_name}'s enrollment_year to 2023")
    session.close()


def task2_delete_enrollment():
    """86: Delete an enrollment record"""
    session = Session()
    enrollment = session.query(Enrollment).filter_by(student_id=2, course_id=1).first()
    if enrollment:
        session.delete(enrollment)
        session.commit()
        print(f"\n Deleted enrollment: student_id=2, course_id=1")
    session.close()


# ── Task 3: Eager Loading — Fix the N+1 Problem ───────────────────────────────

def task3_read_enrollments_joinedload():
    """
    88: Fixed with joinedload — all data fetched in 1 SQL statement.
    Compare the echo=True output with task2_read_enrollments_naive().
    """
    session = Session()
    print("\n── Enrollments (OPTIMISED — joinedload) ─────────")
    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course)
        )
        .all()
    )
    # No extra queries fired here — data already loaded via JOIN
    for e in enrollments:
        print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | Grade: {e.grade}")
    session.close()


# ── Run all tasks ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("TASK 2: CRUD Operations")
    print("=" * 55)
    task2_insert_data()
    task2_read_cs_students()

    print("\n" + "=" * 55)
    print("TASK 2 Step 84: NAIVE (N+1) — count SQL statements in echo output")
    print("=" * 55)
    task2_read_enrollments_naive()

    task2_update_student()
    task2_delete_enrollment()

    print("\n" + "=" * 55)
    print("TASK 3: OPTIMISED with joinedload — should be 1 SQL statement")
    print("=" * 55)
    task3_read_enrollments_joinedload()

    print("\nDone. Compare the number of SQL statements in the echo output above.")
    print("   Naive approach: N+1 queries (one per enrollment for student + course)")
    print("   joinedload:     1 query with LEFT OUTER JOINs — all data in one shot")
