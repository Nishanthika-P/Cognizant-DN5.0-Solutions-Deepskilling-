"""
models.py
Hands-On 7, Task 1, step 72: full schema - Department, Course, Student,
Enrollment - so Students/Enrollments CRUD can follow the same pattern
as Course.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100))
    budget = Column(Numeric(12, 2))

    courses = relationship('Course', back_populates='department')
    students = relationship('Student', back_populates='department')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='courses')


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    enrollment_year = Column(Integer)

    department = relationship('Department', back_populates='students')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(Date, server_default=func.current_date())
    grade = Column(String(2), nullable=True)

    student = relationship('Student')
    course = relationship('Course')


class User(Base):
    """Hands-On 9, Task 1, step 86: registered API user."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)  # 1 = True, 0 = False (SQLite-friendly)
