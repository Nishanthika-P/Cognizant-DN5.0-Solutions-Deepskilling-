"""
main.py
Hands-On 7 - FastAPI: Dependency Injection, CRUD & OpenAPI Documentation.

Task 1: complete Course CRUD with proper status codes + response models,
        HTTPException 404s, /students/ join endpoint, full CRUD for
        Students and Enrollments.
Task 2: BackgroundTasks on enrollment creation, OpenAPI metadata
        customisation, tags, summary/response_description.
"""
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course as CourseModel, Student as StudentModel, Enrollment as EnrollmentModel
from schemas import (
    CourseCreate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)

# ---------------------------------------------------------------
# Task 2, step 75: OpenAPI metadata customisation
# ---------------------------------------------------------------
app = FastAPI(
    title='Course Management API',
    description='Backend API for managing departments, courses, students, '
                'and enrollments - Digital Nurture 5.0 Hands-On 7.',
    version='1.0.0',
    contact={'name': 'Digital Nurture 5.0 POC', 'email': 'poc@college.edu'},
)


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def send_confirmation_email(student_email: str):
    """Task 2, step 73: simulated background task - not awaited by the client."""
    print(f'Sending confirmation to {student_email}')


# ---------------------------------------------------------------
# Courses (Task 1, step 68-71) - tags: step 76
# ---------------------------------------------------------------
@app.post(
    '/api/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The newly created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'])
async def list_courses(
    skip: int = 0, limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(CourseModel)
    if department_id is not None:
        query = query.where(CourseModel.department_id == department_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    existing = result.scalar_one_or_none()
    if existing is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for field, value in course.model_dump().items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@app.delete(
    '/api/courses/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Courses'],
)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()


@app.get(
    '/api/courses/{course_id}/students/',
    response_model=List[StudentResponse],
    tags=['Courses'],
)
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    """Task 1, step 71: JOIN Enrollment -> Student for a given course."""
    result = await db.execute(
        select(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .where(EnrollmentModel.course_id == course_id)
    )
    return result.scalars().all()


# ---------------------------------------------------------------
# Students (Task 1, step 72 - same CRUD pattern)
# ---------------------------------------------------------------
@app.post('/api/students/', response_model=StudentResponse, status_code=201, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get('/api/students/', response_model=List[StudentResponse], tags=['Students'])
async def list_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).offset(skip).limit(limit))
    return result.scalars().all()


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.delete('/api/students/{student_id}', status_code=204, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    await db.delete(student)
    await db.commit()


# ---------------------------------------------------------------
# Enrollments (Task 1, step 72 + Task 2, step 73-74: background task)
# ---------------------------------------------------------------
@app.post(
    '/api/enrollments/',
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
    summary='Enroll a student in a course',
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    # Verify the student exists so we can grab their email for the background task
    result = await db.execute(select(StudentModel).where(StudentModel.id == enrollment.student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')

    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    # Task 2, step 73: response returns immediately (201); email is sent after
    background_tasks.add_task(send_confirmation_email, student.email)

    return new_enrollment


@app.get('/api/enrollments/', response_model=List[EnrollmentResponse], tags=['Enrollments'])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EnrollmentModel))
    return result.scalars().all()
