"""
schemas.py
Hands-On 6, Task 1, steps 58-59: Pydantic request/response schemas.
"""
from typing import Optional, List
from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: Optional[int] = None


class CourseCreate(CourseBase):
    """Used for POST /api/courses/ - all fields required except department_id."""
    pass


class CourseUpdate(BaseModel):
    """Used for PUT/PATCH - every field optional, only supplied ones are updated."""
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(CourseBase):
    """Response schema - includes the DB-generated id."""
    id: int

    class Config:
        from_attributes = True  # allows creation from ORM objects


class DepartmentResponse(BaseModel):
    """Task 1, step 59: nested Pydantic model demonstration."""
    id: int
    name: str
    head_of_dept: Optional[str] = None
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True
