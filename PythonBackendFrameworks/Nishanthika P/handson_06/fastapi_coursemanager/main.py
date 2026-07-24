"""
main.py
Hands-On 6:
  Task 1 - FastAPI app setup, root route, POST /api/courses/ with
           Pydantic validation (step 57, 60), /docs Swagger UI (step 61).
  Task 2 - path/query params, pagination + filtering, async DB access
           via Dependency Injection (steps 62-67).
"""
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course as CourseModel
from schemas import CourseCreate, CourseResponse

app = FastAPI(title='Course Management API', version='1.0')


@app.on_event('startup')
async def on_startup():
    # Creates tables on startup (adequate for this hands-on; use Alembic
    # migrations for anything beyond a learning exercise).
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
async def root():
    return {'message': 'API running'}


# ---------------------------------------------------------------
# Task 1, step 60: POST with Pydantic validation (422 on bad input)
# ---------------------------------------------------------------
@app.post('/api/courses/', response_model=CourseResponse, status_code=201)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


# ---------------------------------------------------------------
# Task 2, step 62: path parameter, auto-validated as int
# ---------------------------------------------------------------
@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


# ---------------------------------------------------------------
# Task 2, step 63/67: query params - pagination + filtering
# ---------------------------------------------------------------
@app.get('/api/courses/', response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(CourseModel)
    if department_id is not None:
        query = query.where(CourseModel.department_id == department_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


# ---------------------------------------------------------------
# Task 2, step 66: full async CRUD - update and delete
# ---------------------------------------------------------------
@app.put('/api/courses/{course_id}', response_model=CourseResponse)
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


@app.delete('/api/courses/{course_id}', status_code=204)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    await db.delete(course)
    await db.commit()
