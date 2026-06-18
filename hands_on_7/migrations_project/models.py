"""
Hands-On 7: Migrations & Versioning — SQLAlchemy Models
Digital Nurture 5.0 | Module 3 | Database Integration

"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date,
    Numeric, Boolean, Time, create_engine
)
from sqlalchemy.orm import relationship, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


# ─────────────────────────────────────────────
# Model Definitions
# ─────────────────────────────────────────────

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))                # renamed from hod_name (Hands-On 1)
    budget        = Column(Numeric(12, 2))

    # Relationships
    students    = relationship("Student",    back_populates="department")
    courses     = relationship("Course",     back_populates="department")
    professors  = relationship("Professor",  back_populates="department")

    def __repr__(self):
        return f"<Department id={self.department_id} name='{self.dept_name}'>"


class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)

    # ── Added in Migration 2 ──────────────────
    is_active = Column(Boolean, default=True)
    # ─────────────────────────────────────────

    # Relationships
    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student id={self.student_id} name='{self.first_name} {self.last_name}'>"


class Course(Base):
    __tablename__ = "courses"

    course_id   = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits     = Column(Integer)
    max_seats   = Column(Integer, default=60)          # added in Hands-On 1 Task 3
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    # Relationships
    department  = relationship("Department",    back_populates="courses")
    enrollments = relationship("Enrollment",    back_populates="course")
    schedules   = relationship("CourseSchedule", back_populates="course")

    def __repr__(self):
        return f"<Course id={self.course_id} code='{self.course_code}'>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(String(2))

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return (f"<Enrollment id={self.enrollment_id} "
                f"student_id={self.student_id} course_id={self.course_id}>")


class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Numeric(10, 2))

    # Relationships
    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor id={self.professor_id} name='{self.prof_name}'>"


# ── Added in Migration 3 ──────────────────────
class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id   = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    day_of_week = Column(String(10), nullable=False)   # e.g., 'Monday'
    start_time  = Column(Time, nullable=False)
    end_time    = Column(Time, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="schedules")

    def __repr__(self):
        return (f"<CourseSchedule id={self.schedule_id} "
                f"course_id={self.course_id} day='{self.day_of_week}'>")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All tables created in college_db_orm.")
