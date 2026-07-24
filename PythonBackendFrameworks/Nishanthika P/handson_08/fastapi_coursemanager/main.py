"""
main.py
Hands-On 8 - RESTful API Design Best Practices (refactor of the
Hands-On 7 FastAPI implementation).

Task 1:
  - /api/v1/ versioning (step 82)
  - plural noun resource naming already in place (/courses/, /students/)
  - PATCH endpoint alongside PUT (step 79)
  - Location header on POST (step 81)
  - correct status codes throughout (step 80)

Task 2:
  - offset pagination envelope: count/next/previous/results (step 83)
  - `search=` filtering on name/code (step 84)
  - standardised {"error": {...}} format via errors.py (step 85)
"""
from typing import Optional, List

from fastapi import FastAPI, Depends, Request, Response, status
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course as CourseModel, Student as StudentModel, Enrollment as EnrollmentModel
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)
from errors import http_exception_handler, not_found
from pagination import Page, build_page
from fastapi import HTTPException

app = FastAPI(
    title='Course Management API',
    description='Versioned, REST-best-practices refactor - Hands-On 8.',
    version='1.0.0',
)

# Task 2, step 85: every HTTPException across the app now returns the
# standardised {"error": {"code", "message", "field"}} envelope.
app.add_exception_handler(HTTPException, http_exception_handler)


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------------------------------------------------------
# NOTE on versioning strategies (Task 2, step 82):
# 1) URL versioning (used here): /api/v1/courses/ - simple, visible,
#    trivially testable in a browser, but every breaking change means
#    a new URL prefix (v2, v3, ...).
# 2) Header-based versioning: keep the URL stable (/api/courses/) and
#    send a version in the Accept header, e.g.
#    "Accept: application/vnd.api+json;version=1". Keeps URLs clean
#    and is common in mature APIs, but harder to test casually (a
#    browser address bar can't set custom headers).
# ---------------------------------------------------------------

V1 = '/api/v1'


# ---------------------------------------------------------------
# Courses
# ---------------------------------------------------------------
@app.post(f'{V1}/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(course: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    # Task 1, step 81: Location header pointing at the new resource
    response.headers['Location'] = f'{V1}/courses/{new_course.id}/'
    return new_course


@app.get(f'{V1}/courses/', response_model=Page, tags=['Courses'])
async def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(CourseModel)
    count_query = select(func.count()).select_from(CourseModel)

    if search:
        # Task 2, step 84: case-insensitive search across name and code
        like = f'%{search}%'
        condition = or_(CourseModel.name.ilike(like), CourseModel.code.ilike(like))
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = (await db.execute(count_query)).scalar_one()

    query = query.offset((page - 1) * page_size).limit(page_size)
    items = (await db.execute(query)).scalars().all()

    serialized = [CourseResponse.model_validate(c).model_dump() for c in items]
    return build_page(serialized, total, request, page, page_size)


@app.get(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise not_found('Course', course_id)
    return course


@app.put(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def replace_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    """PUT - full replace, all fields required."""
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    existing = result.scalar_one_or_none()
    if existing is None:
        raise not_found('Course', course_id)
    for field, value in course.model_dump().items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.patch(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    """Task 1, step 79: PATCH - partial update, only supplied fields change."""
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    existing = result.scalar_one_or_none()
    if existing is None:
        raise not_found('Course', course_id)
    for field, value in course.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.delete(f'{V1}/courses/{{course_id}}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise not_found('Course', course_id)
    await db.delete(course)
    await db.commit()


@app.get(f'{V1}/courses/{{course_id}}/students/', response_model=List[StudentResponse], tags=['Courses'])
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .where(EnrollmentModel.course_id == course_id)
    )
    return result.scalars().all()


# ---------------------------------------------------------------
# Students
# ---------------------------------------------------------------
@app.post(f'{V1}/students/', response_model=StudentResponse, status_code=201, tags=['Students'])
async def create_student(student: StudentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    response.headers['Location'] = f'{V1}/students/{new_student.id}/'
    return new_student


@app.get(f'{V1}/students/', response_model=List[StudentResponse], tags=['Students'])
async def list_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).offset(skip).limit(limit))
    return result.scalars().all()


# ---------------------------------------------------------------
# Enrollments
# ---------------------------------------------------------------
@app.post(f'{V1}/enrollments/', response_model=EnrollmentResponse, status_code=201, tags=['Enrollments'])
async def create_enrollment(enrollment: EnrollmentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    response.headers['Location'] = f'{V1}/enrollments/{new_enrollment.id}/'
    return new_enrollment
