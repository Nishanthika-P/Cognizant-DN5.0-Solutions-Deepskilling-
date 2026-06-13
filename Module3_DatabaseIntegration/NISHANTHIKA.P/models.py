"""
HANDS-ON 6 — Task 1: SQLAlchemy ORM Models
File: models.py
"""

from sqlalchemy import (
    Column, Integer, String, Date, Decimal,
    ForeignKey, create_engine, CHAR
)
from sqlalchemy.orm import relationship, declarative_base

# ── Engine and Base ───────────────────────────────────────────────────────────

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs all SQL
Base   = declarative_base()


# ── ORM Models ────────────────────────────────────────────────────────────────

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Decimal(12, 2))

    # Relationships
    students   = relationship("Student",   back_populates="department")
    courses    = relationship("Course",    back_populates="department")
    professors = relationship("Professor", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.dept_name}')>"


class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50),  nullable=False)
    last_name       = Column(String(50),  nullable=False)
    email           = Column(String(100), nullable=False, unique=True)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)

    # Relationships
    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.first_name} {self.last_name}')>"


class Course(Base):
    __tablename__ = "courses"

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20),  unique=True)
    credits       = Column(Integer)
    max_seats     = Column(Integer, default=60)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    # Relationships
    department  = relationship("Department",  back_populates="courses")
    enrollments = relationship("Enrollment",  back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}')>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(CHAR(2))

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student={self.student_id}, course={self.course_id}, grade={self.grade})>"


class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Decimal(10, 2))

    # Relationships
    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor(id={self.professor_id}, name='{self.prof_name}')>"


# ── Create all tables ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # First create college_db_orm in MySQL:
    # CREATE DATABASE college_db_orm;
    Base.metadata.create_all(engine)
    print("\n All 5 tables created successfully in college_db_orm.")
    print("   Verify in MySQL: USE college_db_orm; SHOW TABLES;")
