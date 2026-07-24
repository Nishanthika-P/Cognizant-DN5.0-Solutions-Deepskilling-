"""
database.py
Hands-On 6, Task 2, step 64: async SQLAlchemy engine + session dependency.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./coursemanager.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    """FastAPI dependency - yields a session, closes it after the request."""
    async with AsyncSessionLocal() as session:
        yield session
