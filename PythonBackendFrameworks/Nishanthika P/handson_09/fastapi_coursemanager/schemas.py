"""
schemas.py
Hands-On 7: Pydantic schemas for Course, Student, Enrollment.
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ---------------------------------------------------------------
# Course
# ---------------------------------------------------------------
class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: Optional[str] = None
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True


# ---------------------------------------------------------------
# Student
# ---------------------------------------------------------------
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None
    enrollment_year: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------------
# Auth (Hands-On 9)
# ---------------------------------------------------------------
class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
